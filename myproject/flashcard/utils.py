import os
from .models import FlashcardKanji, FlashcardList, FlashcardWord, FlashcardKanjiList
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

    def is_kanji(self, char):
        return '\u4e00' <= char <= '\u9fff'
    
    def extractKanji(self, word):
        kanji_list = [char for char in word if self.is_kanji(char)]
        return kanji_list # return a list
    
    def findAndaddKanjiList(self, word):
        # add từ vào extractkanjilist và kanjilist
        extractList = self.extractKanji(word.writing)

        new_kanjiList = self.addKanjiList(word)
        for element in extractList:
            kanji = Kanji(element, 'javi', 'kanji')
            kanji_id = kanji.getMobileId()

            try: #kiểm tra kanji đã từng được tạo trước đây chưa nếu có rồi thì chỉ thêm vào kanjiList
                obj = FlashcardKanji.objects.get(id=kanji_id) 
                obj.kanjilist.add(new_kanjiList)
                # print("đem it")

            except ObjectDoesNotExist: 
                mean = self.getSinoVietnamese(kanji) # lấy âm hán việt
                self.addKanji(kanji_id, element, mean, new_kanjiList)
    
    def getSinoVietnamese(self, kanji): # đầu vào là một object Word
        kanjiMeaning = kanji.getMeaning().get('mean').split(',')
        return kanjiMeaning[0].strip() # Lấy âm hán việt

    def addKanji(self, kanji_id, writing, hanviet, kanjilist):
        return FlashcardKanji.add(kanji_id, writing, hanviet, kanjilist)
    
    def addKanjiList(self, word):
        return FlashcardKanjiList.add(word)

    def addWord(self, word_id, writing, meaning, furigana):
        print(self.list)
        return FlashcardWord.add(word_id, writing, meaning, furigana, self.list.id)

    def addList(self):
        return FlashcardList.add(self.name)

    def add(self, readings):
        # add từ vào wordList
        temp = NonKanji(readings.get('w'), 'javi', 'word')
        word_id = temp.getMobileId()
    
        try: #kiểm tra word đã từng được tạo trước đây chưa
            obj = FlashcardWord.objects.get(id=word_id)
            obj.list.add(self.list)

        except ObjectDoesNotExist: 
            writing = readings.get('w')
            meaning = readings.get('m')
            furigana = readings.get('p')
            new_word = self.addWord(word_id, writing, meaning, furigana)
            self.findAndaddKanjiList(new_word)
            

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

    def getCard(self, word):
        id = word.id
        w = word.writing
        p = word.furigana
        m = word.meaning
        hanviet = ""
        kanjiList = FlashcardKanjiList.objects.filter(word=word).first()
        kanjis = FlashcardKanji.objects.filter(kanjilist=kanjiList)
        for kanji in kanjis:
            hanviet += kanji.hanviet + ' '
        return {
            'id': id,
            'w': w,
            'p': p,
            'm': m,
            'h': hanviet
        }

    def exportToTxt(self):
        setting = "#separator:tab\n#html:false\n"
        filename = self.name + '.txt'
        words = FlashcardWord.objects.filter(list=self.list)
        data = ""
        for word in words:
            card = self.getCard(word)
            w = card.get('w')
            p = card.get('p')
            m = card.get('m')
            hanviet = card.get('h')
            data += f'{w}\t{p}\t{m}\t{hanviet}\n'
        print(setting + data)
        try:
            # Kiểm tra xem file đã tồn tại chưa và thông báo
            if os.path.exists(filename):
                print(f"File {filename} đã tồn tại và sẽ bị ghi đè.")
            else:
                print(f"Tạo mới file {filename}.")

            # Mở file và ghi dữ liệu vào
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(setting + data)
        except IOError as e:
            print(f"Không thể mở hoặc ghi file {filename}: {e}")
    
    def getList(self):
        words = FlashcardWord.objects.filter(list=self.list)
        result = []
        for word in words:
            card = self.getCard(word)
            result.append(card)
        return result