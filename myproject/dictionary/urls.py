from django.urls import path
from .SearchField import searchWordMeaning, searchWordSuggestion
from . import views

urlpatterns = [
    path('', searchWordMeaning, name='search-field'),
    path('suggestions/', searchWordSuggestion, name='suggestions'),
    path('search/<str:pk>/', views.searchWord, name='search-field'),
    path('suggestion/<str:pk>/', views.getSuggestion, name='suggestions')
    # path('kanji-art/', getKanjiArt, name='kanji_art')
]