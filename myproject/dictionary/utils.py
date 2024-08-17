import requests
from .serializers import KanjiSerializer, WordSerializer

def fetchWordMeaning(search_word, lang, search_type):
    url = "https://mazii.net/api/search"
    response = requests.post(url, data={
        'dict': lang,
        'type': search_type,
        'query': search_word,
        'limit': '20',
        'page': '1',
    })
    
    # Check if the request was successful
    if response.status_code != 200:
        return {"error": "Failed to fetch data from the dictionary API"}

    wordData = response.json()
    wordData = wordData.get('data')
    
    # Check if the response contains data
    if not wordData:
        return {"error": "No data found for the given word"}
    
    result = {}
    if wordData == "kanji":
        for i, kanji in enumerate(wordData):
            result[i] = KanjiSerializer(data = kanji)
    else:
        for i, word in enumerate(wordData):
            result[i] = WordSerializer(data = word)
    return result

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