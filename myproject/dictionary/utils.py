from django.http import HttpResponse
import requests
from .serializers import KanjiSerializer, WordSerializer, MaziiWordExampleReturnTypeSerializer
import xml.etree.ElementTree as ET
from django.http import JsonResponse

def fetchWordMeaning(search_word, lang, search_type):
    url = "https://mazii.net/api/search"
    response = requests.post(url, data={
        'dict': lang,
        'type': search_type,
        'query': search_word,
        'limit': '1',
        'page': '1'
    })
    
    # Check if the request was successful
    if response.status_code != 200:
        return {"error": "Failed to fetch data from the dictionary API"}

    wordData = response.json()
    # Check if the response contains data
    if not wordData:
        return {"error": "No data found for the given word"}
    
    result = {}
    comment = {}
    if search_type == "kanji":
        wordData = wordData.get('results')
        for i, kanji in enumerate(wordData):
            result[i] = KanjiSerializer(data = kanji)
            if result[i].is_valid():
                #print(result[i].validated_data.get('mobileId'))
                #print(result[i]['mobileId'].value(), result[i]['kanji'].value())
                comment[i] = fetchComment(result[i])
    else:
        wordData = wordData.get('data')
        for i, word in enumerate(wordData):
            result[i] = WordSerializer(data = word)
    return {
        'result': result,
        'comment': comment
    }

def fetchWordSuggestion(search_word, lang):
    url = 'https://mazii.net/api/suggest'
    response = requests.post(url, data={
        'keyword': search_word,
        'dict': lang
    })

    word_data = response.json()
    print("Received data:", word_data)  # In ra dữ liệu nhận được để kiểm tra
    if word_data.get('status') == 200:
        # Kiểm tra cấu trúc của 'data'
        data_list = word_data.get('data', [])
        if isinstance(data_list, list):
            suggestions = [
                {
                    'kanji': e.split("#")[0],
                    'reading': e.split("#")[1],
                    'meaning': e.split("#")[2]
                } for e in data_list
            ]
            return suggestions
        
def fetchExample(KanjiMeaning):
    url = f'https://mina.mazii.net/api/getNoteKanji.php?word={KanjiMeaning['kanji']}'
    response = requests.get(url)

    if response.status_code == 200:
        example_data = response.json()
        if example_data:
            return {'note': example_data[0].get('note')}
        else:
            return {"error": "No data found for the given word"}
    else:
        return {"error": "Failed to fetch data from external API"}
    
def fetchComment(kanji):
    url = "https://api.mazii.net/api/get-mean"
    #print(kanji['mobileId'], kanji['kanji'])
    response = requests.post(url, json={
        'wordId': kanji.validated_data.get('mobileId'),
        'type': 'kanji',
        'dict': 'javi',
        'word': kanji.validated_data.get('kanji')
    }, headers={'Content-Type': 'application/json'})
    
    if response.status_code != 200:
        return {"error": "Failed to fetch data from the dictionary API"}
    
    comments = response.json()
    if not comments:
        return {"error": "No data found for the given word"}
    comments = comments.get('result')
    return comments

def getExample(word, lang):
    url = "https://mazii.net/api/search"
    response = requests.post(url, data={
        'type': 'example',
        'dict': lang,
        'query': word
    })
    
    result = {}
    if response.status_code == 200:
        exampleData = response.json().get('result')
        for i, example in enumerate(exampleData):
            result[i] = MaziiWordExampleReturnTypeSerializer(data = example)
        return result
    else:
        return {"error": "Failed to fetch data from external API"}
    
def getComment(mobileId, type, lang, word):    
    url = "https://api.mazii.net/api/get-mean"
    response = requests.post(
        url,
        json={
            'wordId': mobileId,
            'type': type,
            'dict': lang,
            'word': word
        },
        headers={'Content-Type': 'application/json'})

    if response.status_code == 200:
        comment_data = response.json()
        comments = comment_data.get('result', [])
        if len(comments) > 5:
            comments = comments[:5]
        return comments
    
    if response.status_code == 304:
        return []
    
    return {'error': 'Failed to fetch comments'}

def unicode_encoding(word):
    # Get the Unicode code point of the first character
    code_point = ord(word)
    # Convert the code point to a hexadecimal string
    hex_code = hex(code_point)[2:]  # Remove the '0x' prefix
    return hex_code

def getKanjiArt(request):
    try:
        # Encode the Kanji character to its Unicode representation
        unicode_kanji = unicode_encoding('漢')
        url = f'https://data.mazii.net/kanji/0{unicode_kanji}.svg'
        print(url)
        # Fetch the SVG data
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        kanji_art_data = response.text

        # Parse the SVG data
        try:
            # You can use ElementTree to parse XML
            root = ET.fromstring(kanji_art_data)
            # If needed, you can extract specific parts from the SVG data here.
            # For simplicity, we'll return the whole SVG data.
            svg_data = ET.tostring(root, encoding='unicode')
            return HttpResponse(svg_data, content_type="image/svg+xml")
        except ET.ParseError as e:
            return JsonResponse({'error': 'Error parsing XML', 'details': str(e)}, status=500)

    except requests.RequestException as e:
        return JsonResponse({'error': 'Error fetching art', 'details': str(e)}, status=500)
