import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag, ne_chunk
from nltk.corpus import stopwords
from typing import List, Tuple

# Baixar recursos do NLTK necessários
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('stopwords')

def process_text_nltk(text: str) -> Tuple[List[List[str]], List[Tuple[str, str]], str]:
    # Tokenizar o texto em sentenças e palavras
    sentences = sent_tokenize(text)
    tokens = [word_tokenize(sentence) for sentence in sentences]

    # Tagging das palavras com suas classes gramaticais
    tagged_tokens = [pos_tag(token) for token in tokens]

    # Reconhecimento de entidades nomeadas
    named_entities = [ne_chunk(tagged) for tagged in tagged_tokens]

    # Filtrando tokens (remover stopwords)
    stop_words = set(stopwords.words('portuguese'))
    filtered_tokens = [[word for word in token if word.lower() not in stop_words] for token in tokens]

    # Extrair entidades nomeadas
    entities = []
    for tree in named_entities:
        for subtree in tree:
            if isinstance(subtree, nltk.Tree):
                entity = " ".join([word for word, tag in subtree.leaves()])
                entities.append((entity, subtree.label()))

    # Gerar HTML para destacar entidades nomeadas
    html = highlight_entities(text, entities)

    return filtered_tokens, entities, html

def highlight_entities(text: str, entities: List[Tuple[str, str]]) -> str:
    """
    Gera um HTML com as entidades nomeadas destacadas.
    """
    # Mapeamento de cores para diferentes tipos de entidades
    colors = {
        'PERSON': 'lightblue',
        'ORGANIZATION': 'lightgreen',
        'LOCATION': 'lightcoral',
        'GPE': 'lightcoral',
        'DATE': 'lightgoldenrodyellow',
        'TIME': 'lightpink'
    }
    
    # Criar um HTML para o texto
    highlighted_text = text
    for entity, label in entities:
        color = colors.get(label, 'lightgray')  # Default color if label not found
        highlighted_text = highlighted_text.replace(entity, f'<span style="background-color: {color};">{entity}</span>')

    html = f"<html><body>{highlighted_text}</body></html>"

    return html

# Exemplo de uso
text = "O João e a Maria foram ao mercado comprar maçãs. A reunião com o Dr. Silva foi agendada para amanhã."
tokens, entities, html = process_text_nltk(text)

print("Tokens:")
print(tokens)
print("\nEntities:")
print(entities)
print("\nHTML:")
print(html)

# Salvando o HTML em um arquivo para visualização
with open("highlighted_entities.html", "w") as file:
    file.write(html)