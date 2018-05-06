
#### dipendenze per wordnet ####
import nltk
from nltk.corpus import wordnet as wn
from pprint import pprint

#imposta il path delle risorse
NLTK_PATH = None # '/home/sergio/ws_ia/mashup/nltk_data'


# categorie supportate
##  sulla base della rete InceptionV3, sono ben supportate le ricognizioni di 
##  dog , cat, forniture, flower
words = [
'canine', 'cat',
'furniture',
'flower',
'plant',
'entity'
]

categories = []


dictService = {}
dictService["canine"] = { 
    "info": "WikiDog", 
    "adotta": "P4HDogAdoption"
}
dictService["cat"] = { 
    "info": "WikiCat", 
    "adotta": "P4HCatAdoption"
}

dictService["furniture"] = { 
    "acquista": "Ikea"
}
dictService["flower"] = { 
    "info": "WikiPlant",
    "acquista": "Crocus"
}
dictService["plant"] = dictService["flower"]


#per una qualsisi altra entita', mostra info di wiki!
dictService["entity"] = { 
    "info": "Wiki",
}





dictAssociatedObject = {}
dictAssociatedObject["canine"] = [
    {
        "objects":["crunchy", "collar"],
        "tag": "petco.com"
    }
]
dictAssociatedObject["cat"] = dictAssociatedObject["canine"]
dictAssociatedObject["furniture"] = []
dictAssociatedObject["flower"] = [
    {
        "objects":["topsoil", "seed"],
        "tag": "crocus"
    }
]
dictAssociatedObject["plant"] = dictAssociatedObject["flower"]

dictAssociatedObject["entity"] = []





def init():
    
    # inizializza la libreria
    if NLTK_PATH == None :
        raise Exception("NLTK data path not specified!")
    else :
        nltk.data.path.append(NLTK_PATH)
    
    # inizializza le categorie
    init_categories()
    

def init_categories():
    for w in words :
        categories.append( wn.synsets(w)[0] )



def find_category(wnid):
    ## restituisci la categoria per la quale la parola passa per essa
    #  Nel caso non trovi una categoria che fa match, allora restituisce 'entity'
    #  (questo perche e' presente nella lista ORDINATA delle categorie, ed e' fissata come ULTIMA!)
    
    entity = wn.synsets('entity')[0]
    
    #wnid e' una strin
    in_word_synset = wn._synset_from_pos_and_offset( wnid[0] , int(wnid[1:]))
    
    pprint("input ==> wnid:" + wnid + "  --> word:" + in_word_synset.name() )
    
    for c in categories:
        pprint("----------> Seleziono la categoria : " + c.name())
        word_cursor = in_word_synset
        while word_cursor != entity :
            
            hypernym = word_cursor.hypernyms()[0]
            
            pprint( c.name() + " e' uguale a " + hypernym.name() + "?   risposta:" + str(hypernym == c) )
            if hypernym.name().split(".")[0] == c.name().split(".")[0] : #check sul nome del synset, tralasciando le varie definizioni (es. n.1 o n.2)
                return c.name()
            
            word_cursor = hypernym
        pprint("------------------------------------------------")



def get_associated_objects( obj ):

    allAssociatedObject = []    
    for s in dictAssociatedObject[obj]:
        allAssociatedObject = allAssociatedObject + s["objects"]
        
    return allAssociatedObject

def get_services_by_object( obj ):
    
    return dictService[obj].keys()




def get_crawler_service(obj, action):
    
    return dictService[obj][action]

def get_tag_url_associated_obj( obj, associated_obj ):
    
    for s in dictAssociatedObject[obj]:
        if associated_obj in s['objects'] :
            return s["tag"]
    
    return None