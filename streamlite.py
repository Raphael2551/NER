import streamlit as st
from spacy_pt_core_news_lg import process_text as spacy_process_text_lg
from spacy_pt_core_news_sm import process_text as spacy_process_text_sm
from transformers_bert_portuguese import process_text_transformers_bert
from transformers_medialbertina_portuguese import process_text_transformers
from transformers_monilouise_portuguese import process_text_transformers_monilouise
from nltk_modelo import process_text_nltk
import base64

# Função para codificar o HTML em base64 para visualização
def get_base64_of_html(html_str):
    return base64.b64encode(html_str.encode()).decode()

# Função para processar o texto com o algoritmo selecionado
def process_text(text, algorithm):
    if algorithm == "spaCy pt_core_news_lg":
        return spacy_process_text_lg(text)
    elif algorithm == "spaCy pt_core_news_sm":
        return spacy_process_text_sm(text)
    elif algorithm == "transformers_medialbertina_portuguese":
        return process_text_transformers(text)
    elif algorithm == "transformers_monilouise_portuguese":
        return process_text_transformers_monilouise(text)
    elif algorithm == "transformers_bert_portuguese":
        return process_text_transformers_bert(text)
    elif algorithm == "nltk":
        return process_text_nltk(text)
    else:
        return [], [], "<html><body><h1>Algoritmo não encontrado</h1></body></html>"

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
st.title("📄 Processamento de Arquivo TXT")

# Seção para upload do arquivo
st.subheader("1. Faça o upload do arquivo")
uploaded_file = st.file_uploader("Escolha um arquivo .txt", type="txt")

# Seção para processamento
if uploaded_file is not None:
    st.subheader("2. Selecione o algoritmo de processamento")

    # Leitura do arquivo
    text = uploaded_file.read().decode("utf-8")

    # Seleção do algoritmo
    algorithm = st.selectbox("Selecione o algoritmo", ["spaCy pt_core_news_lg", "spaCy pt_core_news_sm", "transformers_medialbertina_portuguese", "transformers_monilouise_portuguese", "nltk", "transformers_bert_portuguese"])

    # Exibição do conteúdo do arquivo
    with st.expander("Mostrar conteúdo do arquivo"):
        st.text_area("Conteúdo do arquivo", text, height=200)
    
    # Processa o texto com o algoritmo selecionado
    tokens, entities, html = process_text(text, algorithm)

    st.subheader("Tokens")
    st.write(tokens)

    st.subheader("Entidades Nomeadas")
    st.write(entities)

    # Exibição da visualização das entidades
    st.subheader("Visualização das Entidades")
    st.markdown(f'<iframe src="data:text/html;base64,{get_base64_of_html(html)}" width="100%" height="600px" frameborder="0"></iframe>', unsafe_allow_html=True)

# Rodapé
st.markdown('<div class="footer">Desenvolvido para TCC - 2024</div>', unsafe_allow_html=True)