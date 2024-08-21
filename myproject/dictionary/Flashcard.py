from .models import Example, Reading
from .serializers import ReadingSerializer

def getWordsRelatedToKanji(Word):
    kanjiMeaning = Word.getMeaning().get('meaning')
    temp1 = Word.getExampleKun(kanjiMeaning[0].get('example_kun'))
    temp2 = Word.getExampleOn(kanjiMeaning[0].get('example_on'))
    return {
        'kun': temp1,
        'on': temp2
    }

class Flashcard:
    wordList = []

    def __init__(self):
        # Khởi tạo các thuộc tính
        self.wordList = []

    def addWord(self, word):
        self.wordList.append(word)
        

    def getWord(self, Word):
        if type(Word).__name__ == 'Kanji':
            kanjiMeaning = Word.getMeaning().get('result')
            kanji = {
                'kanji': kanjiMeaning.get('example')
            }
    
    def addWordsRelatedToKanji(self, word, num_vocab):
        # Lấy data
        exampleKun = getWordsRelatedToKanji(word).get('kun')
        exampleOn = getWordsRelatedToKanji(word).get('on')

        # Xử lý ví dụ Kunyomi
        for _, readings in exampleKun:
            for i in range(num_vocab, len(readings)):
                self.addWord(readings[i])
        
        # Xử lý ví dụ Onyomi
        for _, readings in exampleOn:
            for i in range(num_vocab, len(readings)):
                self.addWord(readings[i])  
