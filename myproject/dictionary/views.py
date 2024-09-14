from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import NonKanji, Kanji, Word

@api_view(['GET'])
def searchWord(request, pk):
    if request.method == 'GET':
        word = NonKanji(pk, 'javi', 'word')
        result = {
            'mobileId': word.mobileId,
            'meaning': word.getMeaning(),
            'example': word.getExample(),
            'comment': word.getComment()
        }
        return Response(result)
    
@api_view(['GET'])
def getImg(request, pk):
    if request.method == 'GET':
        word = NonKanji(pk, 'javi', 'word')
        result = word.getImg()
        return Response(result)
    
@api_view(['GET'])
def searchKanji(request, pk):
    if request.method == 'GET':
        kanji = Kanji(pk, 'javi', 'kanji')
        result = {
            'meaning': kanji.getMeaning(),
            'example': kanji.getExample(),
            'comment': kanji.getComment(),
            'kanjiArt': kanji.getKanjiArt(),
        }
        return Response(result)
    
@api_view(['GET'])
def getSuggestion(request, pk):

    if request.method == 'GET':
        word = Word(pk)
        return Response(word.getSuggestion())