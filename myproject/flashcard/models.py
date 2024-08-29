from django.db import models

# Create your models here.
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