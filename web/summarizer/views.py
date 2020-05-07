from django.shortcuts import render
from django.http import HttpResponse
from validator_collection import validators, checkers


import nltk
import transformers
from transformers import pipeline
from newspaper import Article
from ktrain import text
nltk.download('punkt')

def accueil(request):
    return render(request, "summarizer/accueil.html") 
 


def resumeur(request):
    input_texte = request.POST['input_texte']
    #try:
    if checkers.is_url(input_texte):
        url = input_texte
        article_dico = article_extraction(url)
            #article_dico["summary_2"] = ktrain_texte_resumeur(article_dico["texte"], lang='fr')
            
        #else:
            #pass
    #except: pass
    return render(request, "summarizer/result.html", article_dico) 


def article_extraction(url, lang='fr'):

    """
    Utilise la bibliothèque newspaper3k pour extraire l'article de journal situé à l'adresse url spécifiée en arguments.
    On récupère le titre, le corps de texte, un résumé et une liste de mots clefs de l'article.
    On retourne ces informations sous la forme d'un dictionaire.
    """

    article = Article(url, language=lang)
    article.download() 
    article.parse() 
    article.nlp() 
    title = article.title
    text = article.text
    summary = article.summary
    summary_2 = ktrain_texte_resumeur(text, lang='fr')
    keywords = article.keywords
    article_dico = {'title':title, 'texte':text, 'summary':summary, 'summary_2':summary_2, 'keywords': keywords}

    return article_dico


def ktrain_texte_resumeur(input_texte, lang='fr'):
    ts = text.TransformerSummarizer()
    output_texte = ts.summarize(input_texte)
    return output_texte

"""
def huggingface_texte_resumeur(input_texte, lang='fr'):
    summarizer = pipeline("summarization", model="t5-small", tokenizer="camembert-base", framework="tf")



def texte_resumeur(input_texte, lang='fr'):
"""