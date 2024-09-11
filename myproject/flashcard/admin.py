from django.contrib import admin
from .models import FlashcardList, FlashcardWord, FlashcardKanji, FlashcardKanjiList

# Register your models here.
admin.site.register(FlashcardList)
admin.site.register(FlashcardWord)
admin.site.register(FlashcardKanji)
admin.site.register(FlashcardKanjiList)