"""Punto de entrada principal y de interfaz de usuario para el agente."""

import streamlit as st

from helpers import (
    create_vector_index,
    generate_answer,
    load_pdf_documents,
    split_documents,
)
from models import create_embeddings, create_llm


@st.cache_resource(show_spinner=False)
def initialize_system():
    """Inicializa los componentes del sistema RAG y los mantiene en caché."""
    docs = load_pdf_documents("datos")
    chunks = split_documents(docs)
    embeddings = create_embeddings()
    vector_store = create_vector_index(chunks, embeddings)
    llm = create_llm()
    return vector_store, llm


def main() -> None:
    """Interfaz de usuario construida con Streamlit."""
    st.set_page_config(page_title="Agente Mercado Central", page_icon="🛒")
    st.title("🛒 Asistente Mercado Central 24h")
    st.write(
        "¡Hola! Soy el agente de IA de Mercado Central 24h. "
        "Hazme preguntas sobre las políticas, operaciones y servicios."
    )

    with st.spinner("Cargando base de conocimiento..."):
        try:
            vector_store, llm = initialize_system()
        except Exception as error:
            st.error(f"Ocurrió un error al cargar el sistema: {error}")
            st.stop()

    query = st.text_input("Ingresa tu consulta:")

    if st.button("Consultar") and query.strip():
        with st.spinner("Analizando documentos corporativos..."):
            try:
                respuesta = generate_answer(query, vector_store, llm)
                st.markdown("### Respuesta del Agente:")
                st.info(respuesta)
            except Exception as error:
                st.error(f"Error al generar la respuesta: {error}")


if __name__ == "__main__":
    main()