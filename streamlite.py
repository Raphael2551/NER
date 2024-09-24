import streamlit as st
from nltk_modelo import process_text_nltk
from spacy_pt_core_news_sm import process_text as spacy_process_text_sm
from spacy_pt_core_news_lg import process_text as spacy_process_text_lg
from transformers_bert_portuguese import process_text_transformers_bert
from transformers_medialbertina_portuguese import process_text_transformers_medialbertina
from transformers_monilouise_portuguese import process_text_transformers_monilouise
import base64

# Função para codificar o HTML em base64 para visualização
def get_base64_of_html(html_str):
    return base64.b64encode(html_str.encode()).decode()

# Função para processar o texto com o algoritmo selecionado
def process_text(text, algorithm):
    if algorithm == "spaCy: pt_core_news_lg":
        return spacy_process_text_lg(text)
    elif algorithm == "spaCy: pt_core_news_sm":
        return spacy_process_text_sm(text)
    elif algorithm == "transformers: medialbertina_portuguese (especialista) ⭐":
        return process_text_transformers_medialbertina(text)
    elif algorithm == "transformers: monilouise_portuguese":
        return process_text_transformers_monilouise(text)
    elif algorithm == "transformers: bert_portuguese":
        return process_text_transformers_bert(text)
    elif algorithm == "nltk: padrao_ingles":
        return process_text_nltk(text)
    else:
        return [], [], "<html><body><h1>Algoritmo não encontrado</h1></body></html>", {}, 0

# Estilizando a interface
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f5f5;
        padding: 20px;
    }
    .stFileUploader, .stButton, .stSelectbox {
        background-color: #DDEBF7;
        border: 1px solid #6095BC;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 20px;
    }
    h1 {
        color: #2C3E50;
        text-align: center;
        font-family: 'Arial', sans-serif;
    }
    .footer {
        text-align: center;
        font-size: 12px;
        color: #aaaaaa;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título da interface
st.title("📄 Extração de Entidades Nomeadas")

# Seção para upload do arquivo
st.subheader("1. Faça o upload do arquivo")
uploaded_file = st.file_uploader("Escolha um arquivo .txt", type="txt")

# Seção para processamento
if uploaded_file is not None:
    try:
        # Leitura do arquivo com a codificação UTF-8
        text = uploaded_file.read().decode("utf-8")

        # Exibição do conteúdo do arquivo
        with st.expander("Mostrar conteúdo do arquivo"):
            st.text_area("Conteúdo do arquivo", text, height=200)

        st.subheader("2. Selecione o algoritmo de processamento")

        # Seleção do algoritmo com destaque na opção especialista
        algorithm = st.selectbox("Selecione o algoritmo", [
            "Selecione...",
            "nltk: padrao_ingles", 
            "spaCy: pt_core_news_lg", 
            "spaCy: pt_core_news_sm",
            "transformers_bert_portuguese",
            "transformers: monilouise_portuguese",
            "transformers: medialbertina_portuguese (especialista) ⭐"
        ])

        # Processa o texto apenas quando um algoritmo for selecionado
        if algorithm != "Selecione...":
            tokens, entities, html, entity_counts, total_entities = process_text(text, algorithm)

            st.subheader("Tokens")
            st.write(tokens)

            st.subheader("Entidades Nomeadas")
            st.write(entities)

            # Exibição da visualização das entidades
            st.subheader("Visualização das Entidades")
            st.markdown(f'<iframe src="data:text/html;base64,{get_base64_of_html(html)}" width="100%" height="600px" frameborder="0"></iframe>', unsafe_allow_html=True)

            # Exibição da contagem de entidades e total
            st.write(f"### Total de Entidades: {total_entities}")
            for entity_type, count in entity_counts.items():
                st.write(f"- **{entity_type}:** {count}")

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")

# Rodapé
st.markdown('<div class="footer">Desenvolvido para TCC - 2024</div>', unsafe_allow_html=True)