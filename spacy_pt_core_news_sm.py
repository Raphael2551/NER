import spacy
from spacy import displacy

# Função para processar o texto e retornar tokens e entidades
def process_text(text):
    # Carregar o modelo grande de português do spaCy
    nlp = spacy.load("pt_core_news_sm")
    
    # Processar o texto com o modelo
    doc = nlp(text)
    
    # Gerar HTML para a visualização das entidades
    html = displacy.render(doc, style="ent", page=True)
    
    # Extrair tokens e entidades
    tokens = [token.text for token in doc]
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    return tokens, entities, html