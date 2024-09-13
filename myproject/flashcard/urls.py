from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.getLists, name='all_list'),
    path('<str:pk>/', views.getListDetail, name='list_detail'),
    path('word/<str:pk>/update/', views.updateWord, name='update_word'),
    path('word/delete/', views.deleteWord, name='delete_word'),
    path('word/create/', views.createWord, name='create_word'),
    path('list/create/', views.createList, name='create_list'),
    # path('kanji-art/', getKanjiArt, name='kanji_art')
]