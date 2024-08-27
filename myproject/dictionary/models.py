from django.db import models

class WordExample(models.Model):
    transcription = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    mean = models.TextField(blank=True, null=True)
    
class Comment(models.Model):
    mean = models.TextField()

class WordMeaning(models.Model):
    short_mean = models.CharField(max_length=255, null=True, blank=True)
    mobileId = models.IntegerField(default=0, blank=True, null=True) 
    word =  models.CharField(max_length=255, null=True, blank=True)
    phonetic = models.CharField(max_length=255, null=True, blank=True)
    means = models.JSONField(default=dict, blank=True, null=True)

class OverallExample(models.Model):
    w = models.CharField(max_length=255, null=True, blank=True)  # meaning in Vietnamese
    m = models.CharField(max_length=255, null=True, blank=True)  # word original
    h = models.CharField(max_length=255, null=True, blank=True)  # word kanji reading
    p = models.CharField(max_length=255, null=True, blank=True)  # word furigana

class KanjiMeaning(models.Model):
    kanji = models.CharField(max_length=255, null=True, blank=True)  # original kanji
    mean = models.CharField(max_length=255, null=True, blank=True)  # kanji meaning in short way
    kun = models.CharField(max_length=255, null=True, blank=True)  # kunyomi
    on = models.CharField(max_length=255, null=True, blank=True)  # onyomi
    detail = models.TextField(blank=True, null=True)  # fully meaning of kanji
    examples = models.JSONField(default=dict, blank=True, null=True)
    example_on = models.JSONField(default=dict, blank=True, null=True)
    example_kun = models.JSONField(default=dict, blank=True, null=True)
    mobileId = models.IntegerField(default=0, blank=True, null=True)  # wordID to pass in another params
    stroke_count = models.IntegerField(default=0, blank=True, null=True)  # kanji stroke count
    level = models.JSONField(default=dict, blank=True, null=True)

class Example(models.Model):
    character = models.CharField(max_length=10, unique=True, blank=True, null=True)
    readings = models.ManyToManyField('Reading', related_name='kanji')
    
    def __str__(self):
        return f'{self.character} {self.readings}'

class Reading(models.Model):
    w = models.CharField(max_length=200, blank=True, null=True)
    m = models.CharField(max_length=200, blank=True, null=True)
    p = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.w} ({self.p}) {self.m}'
    
class FlashcardList(models.Model):
    list_id = models.AutoField(primary_key=True, unique=True)
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
    list = models.ForeignKey(FlashcardList, on_delete=models.CASCADE)

    @classmethod
    def add(cls, id=None, writing=None, meaning=None, furigana=None, list=None):
        # Kiểm tra xem đối tượng đã tồn tại chưa
        temp, created = cls.objects.get_or_create(id=id, defaults={
            'writing': writing,
            'meaning': meaning,
            'furigana': furigana,
            'list': list
        })
        if created:
            # Nếu đối tượng mới được tạo, thực hiện thêm logic nếu cần
            pass
        return temp

class FlashcardKanji(models.Model):
    id = models.CharField(max_length=10, unique=True, primary_key=True, default='None')
    writing = models.CharField(max_length=100, null=True, blank=True)
    hanviet = models.CharField(max_length=100, null=True, blank=True)
    word = models.ForeignKey(FlashcardWord, on_delete=models.CASCADE)

    @classmethod
    def add(cls, id=None, writing=None, hanviet=None, word=None):
        # Kiểm tra xem đối tượng đã tồn tại chưa
        temp, created = cls.objects.get_or_create(id=id, defaults={
            'writing': writing,
            'hanviet': hanviet,
            'word': word
        })
        if created:
            # Nếu đối tượng mới được tạo, thực hiện thêm logic nếu cần
            pass
        return temp