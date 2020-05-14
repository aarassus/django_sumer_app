from django.shortcuts import render
from transformers import AutoConfig, AutoTokenizer, AutoModel
from summarizer import Summarizer


def accueil(request):
    """
    INPUT:
        Objet request : On récupère s'ils existent 'input_texte' et 'ratio_percent' grâce à la méthode POST
        input_texte : str - il s'agit du texte que l'on souhaite résumer
        ratio_percent : int (compris entre 5 et 100) pourcentage de réduction du texte, si ratio_percent = 50 on va garder 50% des phrases du texte d'origine
    
    OUTPUT:
        dico: dict - {'input_texte': str texte d'origine ,'summary_texte': str texte résumé , 'ratio_percent': int pourcentage de réduction}
    """
    try:
        input_texte = request.POST['input_texte']
        ratio_percent = request.POST['ratio_percent']
        dico = texte_summarizer(input_texte, ratio=float(int(ratio_percent)/100))
        dico.update({'input_texte':input_texte, 'ratio_percent':ratio_percent})
    except:
        dico={'input_texte':'Coller ici le texte que vous souhaitez résumer.', 'ratio_percent': 25}
    return render(request, "summarizer_app/accueil.html", dico) 
 

def texte_summarizer(input_texte, ratio=0.5):
    """
    INPUT:
        input_texte : str - il s'agit du texte que l'on souhaite résumer
        ratio : float (compris entre 0 et 1) - pourcentage de réduction du texte, si ratio = 0.5 on va garder 50% des phrases du texte d'origine

    OUTPUT:
        dico : dict - {'summary_texte' : str result} avec result le texte résumé

    BODY:
        On charge depuis le dossier static/model le modele de NLP à utiliser puis on l'applique au texte à résumer
    """
    custom_config = AutoConfig.from_pretrained("static/model/camembert-base")
    custom_config.output_hidden_states=True
    custom_tokenizer = AutoTokenizer.from_pretrained("static/model/camembert-base")
    custom_model = AutoModel.from_pretrained("static/model/camembert-base", config=custom_config )
    model = Summarizer(custom_model=custom_model, custom_tokenizer=custom_tokenizer,)
    result = model(input_texte, ratio=ratio)
    dico = {'summary_text': result}
    return dico