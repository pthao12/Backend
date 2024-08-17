from django import forms

class SearchForm(forms.Form):
    search_word = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Enter word to search'})
    )
    lang = forms.ChoiceField(
        choices=[
            ('javi', 'Japanese to Vietnamese'),
            ('jaen', 'Japanese to English')
        ],
        initial='javi',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    type = forms.ChoiceField(
        choices=[
            ('kanji', 'Kanji'),
            ('word', 'Word')
        ],
        initial='word',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class SuggestionsForm(forms.Form):
    search_word = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Enter word to search'})
    )
    lang = forms.ChoiceField(
        choices=[
            ('javi', 'Japanese to Vietnamese'),
            ('jaen', 'Japanese to English')
        ],
        initial='javi',
        widget=forms.Select(attrs={'class': 'form-control'})
    )