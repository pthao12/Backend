from django.urls import path
from .SearchField import searchWordMeaning, searchWordSuggestion
from . import views

urlpatterns = [
    path('', searchWordMeaning, name='search-field'),
    path('suggestions/', searchWordSuggestion, name='suggestions'),
    path('search/word/<str:pk>/', views.searchWord),
    path('search/kanji/<str:pk>/', views.searchKanji),
    path('suggestion/<str:pk>/', views.getSuggestion, name='suggestions'),
    path('img/<str:pk>/', views.getImg),
    # path('kanji-art/', getKanjiArt, name='kanji_art')
]