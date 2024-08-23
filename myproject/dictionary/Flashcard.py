from .models import Example, Reading
from .serializers import ReadingSerializer
from .utils import Word, Kanji, NonKanji

def getWordsRelatedToKanji(Word):
    kanjiMeaning = Word.getMeaning()
    kunData = Word.getExampleKun(kanjiMeaning.get('example_kun'))
    onData = Word.getExampleOn(kanjiMeaning.get('example_on'))
    return {
        'kun': kunData,
        'on': onData
    }

def append_if_not_exists(lst, item):
    if item not in lst:
        lst.append(item)

class Flashcard:
    wordList = []
    kanjiList = []
    extractKanjiList = []
    list_id = str

    def __init__(self, list_id):
        # Khởi tạo các thuộc tính
        self.list_id = list_id

    #def addWord(self, content, list_id, id):
        # self.wordList.append_if_not_exists((content, list_id, id))
        # return 1
    
    def is_kanji(self, char):
        return '\u4e00' <= char <= '\u9fff'
    
    def extractKanji(self, word):
        kanji_list = [char for char in word if self.is_kanji(char)]
        return kanji_list # return a list
    
    def getSinoVietnamese(self, kanji): # đầu vào là một object Word
        kanjiMeaning = kanji.getMeaning() 
        #print(kanjiMeaning)
        return kanjiMeaning.get('mean') # Lấy âm hán việt
    
    def addExtractKanjiList(self, word_id, kanji_id):
        data = (word_id, kanji_id)
        append_if_not_exists(self.extractKanjiList, data)

    def addKanji(self, kanji_id, word, meaning):
        #meaning = self.getSinoVietnamese(kanji)
        # id = kanji.getMobileId()
        data = (kanji_id, word, meaning)
        append_if_not_exists(self.kanjiList, data)

    def addWordList(self, id, writing, meaning, furigana):
        data = (id, self.list_id, writing, meaning, furigana)
        append_if_not_exists(self.wordList, data)

    def log(self):
        print('Kanji List :')
        print(self.kanjiList)
        print('Word List:')
        print(self.wordList)
        print('Extract Kanji List:')
        print(self.extractKanjiList)

    def addWord(self, readings):
        if readings.get('w') not in self.wordList:
            # add từ vào wordList
            temp = NonKanji(readings.get('w'), 'javi', 'word')
            word_id = temp.getMobileId()
            writing = readings.get('w')
            meaning = readings.get('m')
            furigana = readings.get('p')
            #print(word_id, writing, meaning, furigana)
            self.addWordList(word_id, writing, meaning, furigana)
            
            # add từ vào extractkanjilist và kanjilist
            extractList = self.extractKanji(readings.get('w'))
            #print(extractList)
            for element in extractList:
                kanji = Kanji(element, 'javi', 'kanji')
                mean = self.getSinoVietnamese(kanji) # lấy âm hán việt
                kanji_id = kanji.getMobileId()

                #print(kanji_id, element, mean)
                self.addKanji(kanji_id, element, mean)
                self.addExtractKanjiList(word_id, kanji_id)

    def addWordsRelatedToKanji(self, word, num_vocab): #word là một object Class
        # Lấy data
        relatedWord = getWordsRelatedToKanji(word)
        exampleKun = relatedWord.get('kun')
        exampleOn = relatedWord.get('on')

        #Xử lý ví dụ Kunyomi
        for _, readings in exampleKun:
            for i in range(min(num_vocab, len(readings))):
                self.addWord(readings[i])
        
        #Xử lý ví dụ Onyomi
        for _, readings in exampleOn:
            for i in range(min(num_vocab, len(readings))):
                self.addWord(readings[i])

        self.log()
        return 1

