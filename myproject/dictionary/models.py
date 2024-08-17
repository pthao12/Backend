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

class WordExample(models.Model):
    content = models.TextField()
    mean = models.TextField()
    transcription = models.TextField()

    def __str__(self):
        return self.Kanji.lower()
    
class WordMeaning(models.Model):
    mean = models.CharField(max_length=300)
    examples = models.ManyToManyField(WordExample)

    def __str__(self):
        return self.WordMeaning.lower()

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
    results = models.ManyToManyField(WordExample)
    
    def __str__(self):
        return self.MaziiWordExampleReturnType.lower()

class OverallExample(models.Model):
    m = models.CharField(max_length=255)  # meaning in Vietnamese
    w = models.CharField(max_length=255)  # word original
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
    example_kun = models.ManyToManyField(KunyomiExample)  # example of kunyomi reading
    example_on = models.ManyToManyField(OnyomiExample)  # example of onyomi reading
    example = models.ManyToManyField(OverallExample)  # kanji overall example, include on and kun
    mobileId = models.IntegerField()  # wordID to pass in another params
    stroke_count = models.IntegerField()  # kanji stroke count

    h = models.CharField(max_length=100)
    w = models.CharField(max_length=100)

class MaziiWordKanjiReturnType(models.Model):
    status = models.IntegerField()  # status as a number
    results = models.ManyToManyField(KanjiMeaning)  # list of KanjiMeaning

