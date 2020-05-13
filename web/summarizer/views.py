from django.shortcuts import render
from django.http import HttpResponse
from validator_collection import validators, checkers



import nltk
import transformers
from transformers import WEIGHTS_NAME, CONFIG_NAME, AutoTokenizer, AutoModelWithLMHead, pipeline
from newspaper import Article
from ktrain import text
nltk.download('punkt')

def accueil(request):
    try:
        input_texte = request.POST['input_texte']
        if checkers.is_url(input_texte):
            url = input_texte
            dico = article_extraction(url)
                #article_dico["summary_2"] = ktrain_texte_resumeur(article_dico["texte"], lang='fr')
                
        else:
            dico = texte_resumeur(input_texte)
        #except: pass
            dico.update({'input_texte':input_texte})
        return render(request, "summarizer/accueil.html", dico) 

    except:
        return render(request, "summarizer/accueil.html") 
 


def resumeur(request):
    input_texte = request.POST['input_texte']
    #try:
    if checkers.is_url(input_texte):
        url = input_texte
        dico = article_extraction(url)
            #article_dico["summary_2"] = ktrain_texte_resumeur(article_dico["texte"], lang='fr')
            
    else:
        dico = texte_resumeur(input_texte)
    #except: pass
    return render(request, "summarizer/accueil.html", dico) 


def texte_resumeur(input_texte):
    tokenizer = AutoTokenizer.from_pretrained("/code/summarizer/static/summarizer/model/t5-small")
    model = AutoModelWithLMHead.from_pretrained("/code/summarizer/static/summarizer/model/t5-small")
    summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)
    dico = summarizer(input_texte)[0]
    return dico


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
    #summary_2 = ktrain_texte_resumeur(text, lang='fr')
    keywords = article.keywords
    article_dico = {'title':title, 'texte':text, 'summary':summary, """'summary_2':summary_2,""" 'keywords': keywords}

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