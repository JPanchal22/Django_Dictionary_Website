from django import forms 

class Search(forms.Form):
    # search_word = forms.BoolField(label="Enter a word...", max_length=100)
    # search_word = forms.BooleanField(required=False)
    word = forms.CharField(label="Enter name", max_length=200)
