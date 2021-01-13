from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import Search
from bs4 import BeautifulSoup
import requests

# Create your views here.
def home(response):
    if response.method == "POST":
        form = Search(response.POST)        

        if form.is_valid():
            word = form.cleaned_data["word"]

        word_meaning_link = requests.get("https://www.dictionary.com/browse/" + str(word)).text
        word_syn_ant_link = requests.get("https://www.thesaurus.com/browse/" + str(word)).text
        synonyms = []
        antonyms = []

        try: 
            soup = BeautifulSoup(word_meaning_link, "lxml")
            content = soup.find_all("div", class_="css-1ghs5zt e1q3nk1v3")
            word_meaning = content[0].text
        except: 
            word_meaning = "No Results Found."
            

        try: 
            soup = BeautifulSoup(word_syn_ant_link, "lxml") 
            word_synonyms = soup.find_all("a", class_=["css-1m14xsh eh475bn1", "css-y8q7q9 eh475bn1", "css-1irfus7 eh475bn1"]) 
            for word_synonym in word_synonyms: 
                synonyms.append(word_synonym.text)
        except: 
                synonyms = ["No Results Found."]


        try:
            soup = BeautifulSoup(word_syn_ant_link, "lxml") 
            word_antonyms = soup.find_all("a", class_=["css-1dcngqk eh475bn1", "css-rw8jx1 eh475bn1"])
            for word_antonym in word_antonyms: 
                antonyms.append(word_antonym.text)
        except: 
                antonyms = ["No Results Found."]

        if synonyms == []:
            synonyms = ["No Results Found."]
        if antonyms == []:
            antonyms = ["No Results Found."]

        return render(response, "Dictionary/word_meaning.html", {"word": word, "word_meaning": word_meaning, "synonyms": synonyms, "antonyms": antonyms})

    else: 
        form = Search()

    return render(response, "Dictionary/home.html", {"form":form})

