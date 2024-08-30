from django.shortcuts import redirect, render
from .forms import SearchForm, SuggestionsForm
from django.http import HttpResponse
from .utils import Kanji, NonKanji
from flashcard.utils import Flashcard

def searchWordMeaning(request):
    results = []
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_word = form.cleaned_data.get('search_word')
            lang = form.cleaned_data.get('lang')
            search_type = form.cleaned_data.get('type')
            check = ''
            if search_type == 'kanji':
                results = Kanji(search_word, lang, search_type)
                temp = Flashcard("2")
                temp.deleteWord("正しい")
                temp.addWordsRelatedToKanji(results, 1)
                temp.exportToTxt()
                print('end')
                #check = getWordsRelatedToKanji(results)
            else:
                results = NonKanji(search_word, lang, search_type)
                temp = Flashcard("1")
                temp.addNonKanji(results)
                print('end')
            results = results.getMeaning()
            return HttpResponse(f"<h1>{1}</h1>")
    else:
        return render(request, 'search.html', {'form': SearchForm})
    
def searchWordSuggestion(request):
    if request.method == 'POST':
        form = SuggestionsForm(request.POST)
        if form.is_valid():
            search_word = form.cleaned_data.get('search_word')
            lang = form.cleaned_data.get('lang')
            search_type = form.cleaned_data.get('type')
            if type == 'kanji':
                results = Kanji(search_word, lang, search_type) 
            else:
                results = NonKanji(search_word, lang, search_type) 
            return HttpResponse(f"<h1>{results.getSuggestion()}</h1>")
    else:
        return render(request, 'suggestions.html', {'form': SearchForm})