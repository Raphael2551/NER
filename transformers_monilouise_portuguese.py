from transformers import pipeline
from collections import Counter


def process_text_transformers_monilouise(text):
    # Decodificar para garantir que o texto esteja em UTF-8
    if isinstance(text, bytes):
        text = text.decode('utf-8', errors='ignore')

    try:
        # Carregar o pipeline NER do transformers
        ner_pipeline = pipeline('ner', model='monilouise/ner_news_portuguese', aggregation_strategy='average')
    except Exception as e:
        print(f"Erro ao carregar o pipeline NER: {e}")
        return [], [], "", {}

    # Processar o texto
    try:
        entities = ner_pipeline(text)
    except Exception as e:
        print(f"Erro ao processar o texto: {e}")
        return [], [], "", {}

    # Extrair tokens e entidades
    tokens = text.split()
    entities_ = [(entity['entity_group'], text[entity['start']:entity['end']]) for entity in entities]

    # Contar as entidades por categoria
    entity_counts = Counter(entity[0] for entity in entities_)
    total_entities = len(entities_)

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
            .Diagnostico { background-color: #d9534f; } /* Vermelho escuro */
            .SinalVital { background-color: #5bc0de; } /* Azul claro */
            .Resultado { background-color: #5cb85c; } /* Verde */
            .Medicamento { background-color: #f0ad4e; } /* Laranja */
            .Dosagem { background-color: #0275d8; } /* Azul escuro */
            .Pessoa { background-color: #ff69b4; } /* Rosa */
            .Loc { background-color: #ffa500; } /* Laranja escuro */
            .entity-container {
                display: inline;
            }
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
    for entity in entities:
        start = entity['start']
        end = entity['end']
        entity_type = entity['entity_group']
        
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
        <div class="legend-item"><span class="legend-color Diagnostico"></span> Diagnóstico</div>
        <div class="legend-item"><span class="legend-color SinalVital"></span> Sinal Vital</div>
        <div class="legend-item"><span class="legend-color Resultado"></span> Resultado</div>
        <div class="legend-item"><span class="legend-color Medicamento"></span> Medicamento</div>
        <div class="legend-item"><span class="legend-color Dosagem"></span> Dosagem</div>
        <div class="legend-item"><span class="legend-color Pessoa"></span> Pessoa</div>
        <div class="legend-item"><span class="legend-color Loc"></span> Localização</div>
    </div>
    </body>
    </html>
    """
    
    return tokens, entities_, html, dict(entity_counts), total_entities

# Exemplo de uso
text = "O Sr. Paciente é epiléptico, sendo medicado já há um bom tempo com fenitoína, estando desde então livre das crises. Face a uma infecção lhe foi prescrita doxiciclina."
tokens, entities, html, entity_counts, total_entities = process_text_transformers_monilouise(text)

print(html)  # Ou salve o HTML em um arquivo para visualização
print("Contagem de entidades por categoria:", entity_counts)
print("Total de entidades reconhecidas:", total_entities)