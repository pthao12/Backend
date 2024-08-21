from .models import Example, Reading
from .serializers import ReadingSerializer

def getWordsRelatedToKanji(Word):
    kanjiMeaning = Word.getMeaning().get('meaning')
    temp1 = Word.getExampleKun(kanjiMeaning[0].get('example_kun'))
    temp2 = Word.getExampleOn(kanjiMeaning[0].get('example_on'))
    return {
        'kun': temp1[0],
        'on': temp2[0]
    }

class Flashcard:
    wordList = []

    def __init__(self):
        # Khởi tạo các thuộc tính
        self.wordList = []

    def addWord(self, Word):
        self.wordList.append(Word)
        

    def getWord(self, Word):
        if type(Word).__name__ == 'Kanji':
            kanjiMeaning = Word.getMeaning().get('result')
            kanji = {
                'kanji': kanjiMeaning.get('example')
            }
