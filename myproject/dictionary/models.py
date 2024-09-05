from django.db import models

class WordExample(models.Model):
    transcription = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    mean = models.TextField(blank=True, null=True)
    
class Comment(models.Model):
    mean = models.TextField()
    like = models.IntegerField(default=0, blank=True, null=True) 
    dislike = models.IntegerField(default=0, blank=True, null=True)
    username = models.CharField(max_length=255, null=True, blank=True)

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
    