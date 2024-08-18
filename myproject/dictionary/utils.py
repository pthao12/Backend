import json
from django.http import HttpResponse
import requests
from .serializers import KanjiSerializer, WordSerializer, MaziiWordExampleReturnTypeSerializer
from .models import KanjiMeaning

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
