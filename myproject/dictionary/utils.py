import requests
from .serializers import KanjiSerializer, WordSerializer, ExampleSerializer, CommentSerializer, ReadingSerializer
import xml.etree.ElementTree as ET
from django.http import JsonResponse
from .getImgBySelenium import getImgBySelenium

class Word:
    word: str
    lang: str
    type: str
    mobileId: str

    def __init__(self, word, lang='javi', type=None, mobileId=None):
        # Khởi tạo các thuộc tính
        self.word = word
        self.lang = lang
        self.type = type
        self.mobileId = mobileId
    
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

    def getExample(self):
        url = "https://mazii.net/api/search"
        response = requests.post(url, json={
            'type': 'example',
            'dict': self.lang,
            'query': self.word,
            'limit': 3
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
    
    def getMobileId(self):
        if self.mobileId is None:
            word = self.getMeaning()
        return self.mobileId

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
        
        meaning = KanjiSerializer(data = wordData[0])
        
        if meaning.is_valid():
            meaning = meaning.validated_data
            self.mobileId = meaning.get('mobileId')
            return meaning
        
        return {}
    
    def getComment(self):
        url = "https://api.mazii.net/api/get-mean"
        response = requests.post(url, json={
            'wordId': self.getMobileId(),
            'type': 'kanji',
            'dict': 'javi',
            'word': self.word
        }, headers={'Content-Type': 'application/json'})
        
        if response.status_code != 200:
            return {"error": "Failed to fetch comments"}
        
        commentData = response.json()

        if not commentData:
            return {"error": "No data found for the given word"}
                    
        commentData = commentData.get('result', [])
        commentData = commentData[:3]
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
                return svg_data
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
        
        meaning = WordSerializer(data = wordData[0])
        if meaning.is_valid():
            meaning = meaning.validated_data
            self.mobileId = meaning.get('mobileId')
            return meaning
        # for i, word in enumerate(wordData):
        #     meaning[i] = WordSerializer(data = word)
        #     if meaning[i].is_valid():
        #         meaning[i] = meaning[i].validated_data
        #         self.mobileId = meaning[i].get('mobileId')
        return {}

    def getComment(self):
        url = "https://api.mazii.net/api/get-mean"
        response = requests.post(
            url,
            json={
                'wordId': self.getMobileId(),
                'type': 'word',
                'dict': 'javi',
                'word': self.word
            },
            headers={'Content-Type': 'application/json'})

        if response.status_code != 200:
            return {"error": "Failed to fetch comments"}
        
        commentData = response.json()

        if not commentData:
            return {"error": "No data found for the given word"}
                    
        commentData = commentData.get('result', [])
        commentData = commentData[:3]
        result = {}

        if not commentData:
            return {"error": "No data found for the given word"}
        
        for i, comment in enumerate(commentData):
            result[i] = CommentSerializer(data = comment)
            if result[i].is_valid():
                result[i] = result[i].validated_data

        return result     

    def getImg(self):
        return getImgBySelenium(self.word)

def unicode_encoding(word):
    # Get the Unicode code point of the first character
    code_point = ord(word)
    # Convert the code point to a hexadecimal string
    hex_code = hex(code_point)[2:]  # Remove the '0x' prefix
    return hex_code
