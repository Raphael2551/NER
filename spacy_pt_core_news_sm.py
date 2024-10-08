import spacy
from collections import Counter

# Função para processar o texto e retornar tokens e entidades
def process_text(text):
    # Carregar o modelo pequeno de português do spaCy
    nlp = spacy.load("pt_core_news_sm")

    # Processar o texto com o modelo
    doc = nlp(text)

    # Extrair tokens e entidades
    tokens = [token.text for token in doc]
    entities = [(ent.label_, ent.text) for ent in doc.ents]

    # Contar as entidades por categoria
    entity_counts = Counter(entity[0] for entity in entities)
    total_entities = len(entities)

    # Gerar HTML básico para a visualização
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
            .PER { background-color: #ff69b4; } /* Pessoa */
            .LOC { background-color: #ffa500; } /* Local */
            .ORG { background-color: #5bc0de; } /* Organização */
            .MISC { background-color: #5cb85c; } /* Outros */
            .legend {
                margin-top: 20px;
            }
            .legend-item {
                display: inline-block;
                margin-right: 20px;
            }
            .legend-color {
                width: 12px;
                height: 12px;
                display: inline-block;
                border-radius: 2px;
                margin-right: 5px;
            }
        </style>
    </head>
    <body>
        <p>
    """

    # Adicionar o texto com marcas de entidades
    last_index = 0
    for ent in doc.ents:
        start = ent.start_char
        end = ent.end_char
        entity_type = ent.label_

        # Adicionar texto antes da entidade
        html += text[last_index:start]

        # Adicionar entidade com cor
        html += f"<span class='highlight {entity_type}'>{text[start:end]}</span>"

        last_index = end

    # Adicionar qualquer texto que venha após a última entidade
    html += text[last_index:]
    html += "</p>"

    # Adicionar legenda para as cores das entidades
    html += """
    <div class="legend">
        <div class="legend-item"><span class="legend-color PER"></span> Pessoa</div>
        <div class="legend-item"><span class="legend-color LOC"></span> Local</div>
        <div class="legend-item"><span class="legend-color ORG"></span> Organização</div>
        <div class="legend-item"><span class="legend-color MISC"></span> Outros</div>
    </div>
    </body>
    </html>
    """

    return tokens, entities, html, dict(entity_counts), total_entities

# Exemplo de uso
text = "O Sr. Paciente é epiléptico, sendo medicado já há um bom tempo com fenitoína, e ele vive em São Paulo. A consulta foi marcada para 25 de setembro."
tokens, entities, html, entity_counts, total_entities = process_text(text)

# Para visualização
print(html)  # Ou salve o HTML em um arquivo para visualização
print("Contagem de entidades por categoria:", entity_counts)
print("Total de entidades reconhecidas:", total_entities)