import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag, ne_chunk
from nltk.corpus import stopwords
from typing import List, Tuple, Dict

# Baixar recursos do NLTK necessários
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('stopwords')

def process_text_nltk(text: str) -> Tuple[List[List[str]], List[Tuple[str, str]], str, Dict[str, int], int]:
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

    # Contar as entidades por categoria
    entity_counts = {}
    for _, label in entities:
        entity_counts[label] = entity_counts.get(label, 0) + 1
    
    total_entities = len(entities)

    return filtered_tokens, entities, html, entity_counts, total_entities

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
    
    # Criar o cabeçalho e o estilo do HTML
    html = """
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.5;
            }
            .highlight {
                padding: 2px 4px;
                border-radius: 3px;
                color: #fff;
                font-weight: bold;
            }
            .PERSON { background-color: lightblue; }
            .ORGANIZATION { background-color: lightgreen; }
            .LOCATION { background-color: lightcoral; }
            .GPE { background-color: lightcoral; }
            .DATE { background-color: lightgoldenrodyellow; }
            .TIME { background-color: lightpink; }
        </style>
    </head>
    <body>
        <p>
    """
    
    # Adicionar o texto com marcas de entidades
    last_index = 0
    for entity, label in entities:
        start = text.find(entity, last_index)
        end = start + len(entity)
        
        # Adicionar texto antes da entidade
        html += text[last_index:start]
        
        # Adicionar entidade com cor
        html += f"<span class='highlight {label}'>{entity}</span>"
        
        last_index = end
    
    # Adicionar qualquer texto que venha após a última entidade
    html += text[last_index:]
    html += """
        </p>
    </body>
    </html>
    """

    return html

# Exemplo de uso
text = "O João e a Maria foram ao mercado comprar maçãs. A reunião com o Dr. Silva foi agendada para amanhã."
tokens, entities, html, entity_counts, total_entities = process_text_nltk(text)

print("Tokens:")
print(tokens)
print("\nEntities:")
print(entities)
print("\nEntity Counts:")
print(entity_counts)
print("\nTotal Entities Recognized:")
print(total_entities)

# Salvando o HTML em um arquivo para visualização
with open("highlighted_entities.html", "w") as file:
    file.write(html)

print("\nHTML saved to highlighted_entities.html")