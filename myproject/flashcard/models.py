from django.db import models
import random
import string

# Create your models here.
class FlashcardList(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    

    @classmethod
    def add(cls, name):
        temp, created = cls.objects.get_or_create(name=name, defaults={
            'name': name
        })
        if created:
            # Nếu đối tượng mới được tạo, thực hiện thêm logic nếu cần
            pass
        return temp

class FlashcardWord(models.Model):
    id = models.CharField(max_length=10, unique=True, primary_key=True, default='None')
    writing = models.CharField(max_length=100, null=True, blank=True)
    meaning = models.CharField(max_length=100, null=True, blank=True)
    furigana = models.CharField(max_length=100, null=True, blank=True)
    list = models.ManyToManyField(FlashcardList, related_name='words')

    class Meta:
        unique_together = ('writing', 'meaning', 'furigana')
        
    @classmethod
    def add(cls, id=None, writing=None, meaning=None, furigana=None, list=None):
        if id is None:
            id = cls.generate_unique_id() 

        # Kiểm tra xem đối tượng đã tồn tại chưa
        temp, created = cls.objects.get_or_create(id=id, defaults={
            'writing': writing,
            'meaning': meaning,
            'furigana': furigana
        })
        if created:
            # Nếu đối tượng mới được tạo, thực hiện thêm logic nếu cần
            pass
        # Cập nhật mối quan hệ nhiều-nhiều nếu có danh sách các đối tượng FlashcardList
        temp.list.add(list)
        return temp
    
    @staticmethod
    def generate_unique_id(length=5):
        while True:
            id = ''.join(random.choices(string.digits, k=length))
            if not FlashcardWord.objects.filter(id=id).exists():
                return id

class FlashcardKanjiList(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    word = models.OneToOneField(FlashcardWord, related_name='kanjilist', on_delete=models.CASCADE)

    @classmethod
    def add(cls, word=None):
        # Kiểm tra xem đối tượng đã tồn tại chưa
        temp, created = cls.objects.get_or_create(word=word)
        if created:
            # Nếu đối tượng mới được tạo, thực hiện thêm logic nếu cần
            pass

        # temp.kanjilist.add(word)

        return temp

class FlashcardKanji(models.Model):
    id = models.CharField(max_length=10, unique=True, primary_key=True, default='None')
    writing = models.CharField(max_length=100, null=True, blank=True)
    hanviet = models.CharField(max_length=100, null=True, blank=True)
    kanjilist = models.ManyToManyField(FlashcardKanjiList, related_name='kanjis')

    @classmethod
    def add(cls, id=None, writing=None, hanviet=None, kanjilist=None):
        # Kiểm tra xem đối tượng đã tồn tại chưa
        temp, created = cls.objects.get_or_create(id=id, defaults={
            'writing': writing,
            'hanviet': hanviet
        })
        if created:
            # Nếu đối tượng mới được tạo, thực hiện thêm logic nếu cần
            pass

        temp.kanjilist.add(kanjilist)

        return temp