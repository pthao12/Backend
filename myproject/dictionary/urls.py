from django.urls import path
from .SearchField import fetchWordMeaning, searchWordSuggestion

urlpatterns = [
    path('', fetchWordMeaning, name='search-field'),
    path('suggestions/', searchWordSuggestion, name='suggestions'),
]