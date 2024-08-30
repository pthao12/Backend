from .models import FlashcardKanji, FlashcardList, FlashcardWord
from dictionary.utils import Kanji, NonKanji
from django.core.exceptions import ObjectDoesNotExist

def getWordsRelatedToKanji(Word):
    kanjiMeaning = Word.getMeaning()
    kunData = Word.getExampleKun(kanjiMeaning.get('example_kun'))
    onData = Word.getExampleOn(kanjiMeaning.get('example_on'))
    return {
        'kun': kunData,
        'on': onData
    }

class Flashcard:
    list = FlashcardList
    name = str

    def __init__(self, name):
        # Khởi tạo các thuộc tính
        self.name = name
        self.list = self.addList()

    #def addWord(self, content, list_id, id):
        # self.wordList.append_if_not_exists((content, list_id, id))
        # return 1
    
    def is_kanji(self, char):
        return '\u4e00' <= char <= '\u9fff'
    
    def extractKanji(self, word):
        kanji_list = [char for char in word if self.is_kanji(char)]
        return kanji_list # return a list
    
    def getSinoVietnamese(self, kanji): # đầu vào là một object Word
        kanjiMeaning = kanji.getMeaning().get('mean').split(',')
        return kanjiMeaning[0].strip() # Lấy âm hán việt

    def addKanji(self, kanji_id, writing, hanviet, word):
        print(kanji_id)
        return FlashcardKanji.add(kanji_id, writing, hanviet, word.id)

    def addWord(self, word_id, writing, meaning, furigana):
        print(self.list)
        return FlashcardWord.add(word_id, writing, meaning, furigana, self.list.id)

    def addList(self):
        return FlashcardList.add(self.name)

    # def log(self):
    #     print('Kanji List :')
    #     print(self.kanjiList)
    #     print('Word List:')
    #     print(self.wordList)
    #     print('Extract Kanji List:')
    #     print(self.extractKanjiList)

    def add(self, readings):
        # add từ vào wordList
        temp = NonKanji(readings.get('w'), 'javi', 'word')
        word_id = temp.getMobileId()
        writing = readings.get('w')
        meaning = readings.get('m')
        furigana = readings.get('p')
        #print(word_id, writing, meaning, furigana)
        new_word = self.addWord(word_id, writing, meaning, furigana)
        #print(word_id, writing, meaning, furigana)
        
        # add từ vào extractkanjilist và kanjilist
        extractList = self.extractKanji(readings.get('w'))
        #print(extractList)
        for element in extractList:
            kanji = Kanji(element, 'javi', 'kanji')
            mean = self.getSinoVietnamese(kanji) # lấy âm hán việt
            kanji_id = kanji.getMobileId()

            #print(kanji_id, element, mean)
            self.addKanji(kanji_id, element, mean, new_word)

    def addWordsRelatedToKanji(self, word, num_vocab): #word là một object Class
        # Lấy data
        relatedWord = getWordsRelatedToKanji(word)
        exampleKun = relatedWord.get('kun')
        exampleOn = relatedWord.get('on')

        #Xử lý ví dụ Kunyomi
        for _, readings in exampleKun:
            for i in range(min(num_vocab, len(readings))):
                self.add(readings[i])
        
        #Xử lý ví dụ Onyomi
        for _, readings in exampleOn:
            for i in range(min(num_vocab, len(readings))):
                self.add(readings[i])

        # self.log()
        return 1

    def addNonKanji(self, word):
        wordMeaning = word.getMeaning()
        w = wordMeaning.get('word')
        m = wordMeaning.get('short_mean')
        p = wordMeaning.get('phonetic')
        reading = {
            'w': w,
            'm': m,
            'p': p
        }
        self.add(reading)

    def deleteWord(self, word):
        obj = FlashcardWord.objects.get(writing = word)
        obj.list.remove(self.list)

    def deleteList(self):
        self.list.delete()

    def exportToTxt(self):
        setting = "#separator:tab\n#html:false\n"
        filename = self.name
        words = FlashcardWord.objects.filter(list=self.list)
        data = ""
        for word in words:
            w = word.writing
            p = word.furigana
            m = word.meaning
            hanviet = ""
            kanjiList = FlashcardKanji.objects.filter(word=word)
            for kanji in kanjiList:
                hanviet += kanji.hanviet + ' '
            data += f'{w}\t{p}\t{m}\t{hanviet}\n'
        print(setting + data)