from transformers import pipeline

def process_text_transformers_bert(text):
    try:
        # Carregar o pipeline NER do transformers
        ner_pipeline = pipeline('ner', model='lfcc/bert-portuguese-ner', aggregation_strategy='average')
    except Exception as e:
        print(f"Erro ao carregar o pipeline NER: {e}")
        return [], [], ""

    # Processar o texto
    try:
        entities = ner_pipeline(text)
    except Exception as e:
        print(f"Erro ao processar o texto: {e}")
        return [], [], ""

    # Extrair tokens e entidades
    tokens = text.split()
    entities_ = [(entity['entity_group'], text[entity['start']:entity['end']]) for entity in entities]
    
    # Gerar HTML básico para a visualização
    html = """
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
            }
            .highlight {
                padding: 2px 4px;
                border-radius: 3px;
                color: #fff;
                font-weight: bold;
            }
            .Diagnostico { background-color: #ff9999; }
            .SinalVital { background-color: #99ff99; }
            .Resultado { background-color: #9999ff; }
            .Medicamento { background-color: #ffcc99; }
            .Dosagem { background-color: #ccffcc; }
            .entity-container {
                display: inline;
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
    html += "</p></body></html>"
    
    return tokens, entities_, html

# Exemplo de uso
text = "Diagnóstico de infarto do miocárdio com tempo de atividade protombínica (TAP) 30% abaixo do normal. Medicamento ácido acetilsalicílico, varfarina, e cimetidina foram prescritos."
tokens, entities, html = process_text_transformers_bert(text)
print(html)  # Ou salve o HTML em um arquivo para visualização
