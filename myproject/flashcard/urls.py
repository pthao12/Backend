from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.getLists, name='all_list'),
    path('<str:pk>/', views.getListDetail, name='list_detail'),
    path('word/<str:pk>/update/', views.updateWord, name='update_word')
    # path('kanji-art/', getKanjiArt, name='kanji_art')
]