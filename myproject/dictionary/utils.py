from django.http import HttpResponse
import requests
from .serializers import KanjiSerializer, WordSerializer, ExampleSerializer, CommentSerializer, ReadingSerializer
import xml.etree.ElementTree as ET
from django.http import JsonResponse
from .models import Example, Reading

class Word:
    word: str
    lang: str
    type: str

    def __init__(self, word, lang, type):
        # Khởi tạo các thuộc tính
        self.word = word
        self.lang = lang
        self.type = type
    
    def getWord(self):
        return self.word
    
    def getLang(self):
        return self.lang
    
    def getType(self):
        return self.type

    def getSuggestion(self):
        url = 'https://mazii.net/api/suggest'
        response = requests.post(url, data={
            'keyword': self.word,
            'dict': self.lang
        })

        if response.status_code != 200:
            return {"error": "Failed to fetch data from the dictionary API"}
        
        wordData = response.json()

        if not wordData:
            return {"error": "No data found for the given word"}
        
        data_list = wordData.get('data', [])
        if isinstance(data_list, list):
            suggestions = [
                {
                    'kanji': e.split("#")[0],
                    'reading': e.split("#")[1],
                    'meaning': e.split("#")[2]
                } for e in data_list
            ]
            return suggestions

    def getExample(self, word):
        url = "https://mazii.net/api/search"
        response = requests.post(url, json={
            'type': 'example',
            'dict': self.lang,
            'query': word,
            'limit': '5'
        }, headers={'Content-Type': 'application/json'})

        if response.status_code != 200:
            return {"error": "Failed to fetch data from the dictionary API"}
        
        exampleData = response.json().get('results', [])
        result = {}

        if not exampleData:
            return {"error": "No data found for the given word"}
        
        for i, example in enumerate(exampleData):
            result[i] = ExampleSerializer(data = example)
            if result[i].is_valid():
                result[i] = result[i].validated_data

        return result 
    
    def getComment(self, word):
        pass

    def getMeaning(self):
        pass
    

class Kanji(Word):
    def __init__(self, word, lang, type):
        # Khởi tạo các thuộc tính
        super().__init__(word, lang, type)

    def getMeaning(self):
        url = "https://mazii.net/api/search"
        response = requests.post(url, data={
            'dict': self.lang,
            'type': "kanji",
            'query': self.word,
            'limit': '1'
        })
                
        # Check if the request was successful
        if response.status_code != 200:
            return {"error": "Failed to fetch data from the dictionary API"}

        wordData = response.json().get('results', [])
        # Check if the response contains data
        if not wordData:
            return {"error": "No data found for the given word"}
        
        meaning = {}
        examples = {}
        comments = {}
        for i, kanji in enumerate(wordData):
            meaning[i] = KanjiSerializer(data = kanji)
            if meaning[i].is_valid():
                meaning[i] = meaning[i].validated_data
                examples[i] = self.getExample(meaning[i].get('kanji'))
                comments[i] = self.getComment(meaning[i])
        return {
            'meaning': meaning,
            'examples': examples,
            'comments': comments
        }
    
    def getComment(self, word):
        url = "https://api.mazii.net/api/get-mean"
        response = requests.post(url, json={
            'wordId': word.get('mobileId'),
            'type': 'kanji',
            'dict': 'javi',
            'word': word.get('kanji'),
            'limit': '3'
        }, headers={'Content-Type': 'application/json'})
        
        if response.status_code != 200:
            return {"error": "Failed to fetch comments"}
        
        commentData = response.json()

        if not commentData:
            return {"error": "No data found for the given word"}
                    
        commentData = commentData.get('result', [])
        result = {}

        if not commentData:
            return {"error": "No data found for the given word"}
        
        for i, comment in enumerate(commentData):
            result[i] = CommentSerializer(data = comment)
            if result[i].is_valid():
                result[i] = result[i].validated_data

        return result

    def getExampleKun(self, exampleKunData):
        result = []
        for character, readings in exampleKunData.items():
            temp = {}
            for i, reading in enumerate(readings):
                temp[i] = ReadingSerializer(data = reading)
                if temp[i].is_valid():
                    temp[i] = temp[i].validated_data
            result.append((character, temp))
        return result

    def getExampleOn(self, exampleOnData):
        result = []
        for character, readings in exampleOnData.items():
            temp = {}
            for i, reading in enumerate(readings):
                temp[i] = ReadingSerializer(data = reading)
                if temp[i].is_valid():
                    temp[i] = temp[i].validated_data
            result.append((character, temp))
        return result

    def getKanjiArt(self):
        try:
            unicode_kanji = unicode_encoding(f'{self.word}')
            url = f'https://data.mazii.net/kanji/0{unicode_kanji}.svg'
            
            # Fetch the SVG data
            response = requests.get(url)
            response.raise_for_status()  
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

class NonKanji(Word):
    def __init__(self, word, lang, type):
        # Khởi tạo các thuộc tính
        super().__init__(word, lang, type)
    
    def getMeaning(self):
        url = "https://mazii.net/api/search"
        response = requests.post(url, data={
            'dict': self.lang,
            'type': "word",
            'query': self.word,
            'limit': '1'
        })        
        # Check if the request was successful
        if response.status_code != 200:
            return {"error": "Failed to fetch data from the dictionary API"}

        wordData = response.json().get('data', [])
        # Check if the response contains data
        if not wordData:
            return {"error": "No data found for the given word"}
        
        meaning = {}
        examples = {}
        comments = {}
        for i, word in enumerate(wordData):
            meaning[i] = WordSerializer(data = word)
            if meaning[i].is_valid():
                meaning[i] = meaning[i].validated_data
                examples[i] = self.getExample(meaning[i].get('word'))
                comments[i] = self.getComment(meaning[i])
        return {
            'meaning': meaning,
            'examples': examples,
            'comments': comments
        }

    def getComment(self, word):
        url = "https://api.mazii.net/api/get-mean"
        response = requests.post(
            url,
            json={
                'wordId': word.get('mobileId'),
                'type': 'word',
                'dict': 'javi',
                'word': word.get('word'),
                'limit': '3'
            },
            headers={'Content-Type': 'application/json'})

        if response.status_code != 200:
            return {"error": "Failed to fetch comments"}
        
        commentData = response.json()

        if not commentData:
            return {"error": "No data found for the given word"}
                    
        commentData = commentData.get('result', [])
        result = {}

        if not commentData:
            return {"error": "No data found for the given word"}
        
        for i, comment in enumerate(commentData):
            result[i] = CommentSerializer(data = comment)
            if result[i].is_valid():
                result[i] = result[i].validated_data

        return result     

def unicode_encoding(word):
    # Get the Unicode code point of the first character
    code_point = ord(word)
    # Convert the code point to a hexadecimal string
    hex_code = hex(code_point)[2:]  # Remove the '0x' prefix
    return hex_code
