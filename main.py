from fastapi import FastAPI
from nltk.corpus import wordnet
import requests
import spacy
from bs4 import BeautifulSoup

nlp = spacy.load('en_core_web_sm')

def lemmatizer(word):
    doc = nlp(word)
    lemmatized_tokens = [token.lemma_ for token in doc]
    return lemmatized_tokens


def get_synonyms(term):
    response = requests.get('https://www.thesaurus.com/browse/{}'.format(term))
    soup = BeautifulSoup(response.text, 'lxml')
    soup = soup.find('div', {'class': 'fltPJVdHfRCxJJVuGX8J'})
    return [span.text for span in soup.findAll('a', {'class': 'Bf5RRqL5MiAp4gB8wAZa'})] # 'css-1gyuw4i eh475bn0' for less relevant synonyms


app = FastAPI()

@app.get("/get_synonyms")
def route_synonyms(word : str):

    lemmatized = lemmatizer(word)
    lemmatized = lemmatized[0]

    return {"words": get_synonyms(lemmatized)}
