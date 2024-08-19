from django.urls import path
from .SearchField import searchWordMeaning, searchWordSuggestion

urlpatterns = [
    path('', searchWordMeaning, name='search-field'),
    path('suggestions/', searchWordSuggestion, name='suggestions'),
    # path('kanji-art/', getKanjiArt, name='kanji_art')
]