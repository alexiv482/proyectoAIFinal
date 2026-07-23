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
    """Interfaz de usuario construida con Streamlit y soporte para historial."""
    st.set_page_config(page_title="Agente Mercado Central", page_icon="🛒")
    st.title("🛒 Asistente Mercado Central 24h")

    # Inicializar el historial en la sesión de Streamlit si no existe
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "¡Hola! Soy el agente de IA de Mercado Central 24h. "
                           "Hazme preguntas sobre las políticas, operaciones y servicios."
            }
        ]

    with st.spinner("Cargando base de conocimiento..."):
        try:
            vector_store, llm = initialize_system()
        except Exception as error:
            st.error(f"Ocurrió un error al cargar el sistema: {error}")
            st.stop()

    # Renderizar los mensajes guardados en el historial
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada de texto usando el componente de chat de Streamlit
    if prompt := st.chat_input("Ingresa tu consulta:"):
        # 1. Guardar y mostrar el mensaje del usuario
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2. Formatear el historial para LangChain (omitiendo el saludo inicial)
        chat_history = []
        for msg in st.session_state.messages[1:-1]:
            role_langchain = "human" if msg["role"] == "user" else "ai"
            chat_history.append((role_langchain, msg["content"]))

        # 3. Generar y mostrar la respuesta de la IA
        with st.chat_message("assistant"):
            with st.spinner("Analizando documentos corporativos..."):
                try:
                    respuesta = generate_answer(
                        query=prompt,
                        vector_store=vector_store,
                        llm=llm,
                        chat_history=chat_history
                    )
                    st.markdown(respuesta)
                    # 4. Guardar la respuesta de la IA en el historial
                    st.session_state.messages.append({"role": "assistant", "content": respuesta})
                except Exception as error:
                    st.error(f"Error al generar la respuesta: {error}")


if __name__ == "__main__":
    main()