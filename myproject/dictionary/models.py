from django.db import models

# Create your models here.
JLPT_LEVEL = {1, 2, 3, 4, 5}

class Kanji(models.Model):
    literal = models.CharField(max_length=100)
    stroke_count = models.IntegerField()
    grade = models.IntegerField()
    frequency = models.IntegerField()
    jlpt = models.IntegerField()
    onyomi = models.CharField(max_length=100)
    kunyomi = models.CharField(max_length=100)
    meanings = models.TextField()
    vietnamese = models.TextField()

    def __str__(self):
        return self.Kanji.lower()

class Example(models.Model):
    transcription = models.TextField()
    content = models.TextField()
    mean = models.TextField()
    
class Comment(models.Model):
    mean = models.TextField()

class WordMeaning(models.Model):
    short_mean = models.CharField(max_length=255)
    mobileId = models.IntegerField() 
    word =  models.CharField(max_length=255)
    phonetic = models.CharField(max_length=255)
    means = models.JSONField()

class MaziiWordTranslate(models.Model):
    word = models.CharField(max_length=100, unique=True)
    short_mean = models.CharField(max_length=100, unique=True)
    phonetic = models.CharField(max_length=100, unique=True) 
    means = models.ManyToManyField(WordMeaning)
    mobileId = models.IntegerField()

    def __str__(self):
        return self.MaziiWordTranslate.lower()
    
class MaziiWordMeaningReturnType(models.Model):
    status = models.IntegerField()
    found = models.BooleanField()
    data = models.ManyToManyField(MaziiWordTranslate)

    def __str__(self):
        return self.MaziiWordMeaningReturnType.lower()

class MaziiWordExampleReturnType(models.Model):
    status = models.IntegerField()
    results = models.ManyToManyField(Example)

class OverallExample(models.Model):
    w = models.CharField(max_length=255)  # meaning in Vietnamese
    m = models.CharField(max_length=255)  # word original
    h = models.CharField(max_length=255)  # word kanji reading
    p = models.CharField(max_length=255)  # word furigana

class KunyomiExample(models.Model):
    kunyomi_word = models.CharField(max_length=255)  # kunyomi example
    examples = models.ManyToManyField(OverallExample)  # list of OverallExample

class OnyomiExample(models.Model):
    onyomi_word = models.CharField(max_length=255)  # onyomi example
    examples = models.ManyToManyField(OverallExample)  # list of OverallExample

class KanjiMeaning(models.Model):
    kanji = models.CharField(max_length=255)  # original kanji
    mean = models.CharField(max_length=255)  # kanji meaning in short way
    kun = models.CharField(max_length=255)  # kunyomi
    on = models.CharField(max_length=255)  # onyomi
    detail = models.TextField()  # fully meaning of kanji
    example_kun = models.JSONField(default=list)  # example of kunyomi reading
    example_on = models.JSONField(default=list)  # example of onyomi reading
    examples = models.JSONField(default=list)  # kanji overall example, include on and kun
    mobileId = models.IntegerField()  # wordID to pass in another params
    stroke_count = models.IntegerField()  # kanji stroke count

class MaziiWordKanjiReturnType(models.Model):
    status = models.IntegerField()  # status as a number
    results = models.ManyToManyField(KanjiMeaning)  # list of KanjiMeaning

