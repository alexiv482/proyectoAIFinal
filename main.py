"""Punto de entrada principal y de interfaz de usuario para el agente."""

import os
import base64
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

@st.dialog("👁️ Visor de Documentos", width="large")
def mostrar_pdf(file_path):
    """Abre una ventana emergente para visualizar el PDF y da la opción de descarga."""
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    
    # Incrusta el PDF en un iframe HTML
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
    
    # Botón de descarga opcional
    with open(file_path, "rb") as f:
        st.download_button(
            label="📥 Descargar este documento",
            data=f,
            file_name=os.path.basename(file_path),
            mime="application/pdf"
        )

def main() -> None:
    """Interfaz de usuario construida con Streamlit y soporte para historial."""
    # PLUS DE INTERFAZ: Diseño más ancho y barra lateral
    st.set_page_config(page_title="Agente Mercado Central", page_icon="🛒", layout="wide")

    st.markdown("""
        <style>
        /* Forzar a que la barra lateral contenga los elementos fijos */
        /* will-change crea un bloque de contención para position: fixed */
        section[data-testid="stSidebar"] {
            will-change: transform;
        }

        /* ESPACIO DE SCROLL PARA LA BARRA LATERAL */
        /* Dejamos un margen arriba y abajo para que los documentos no queden ocultos */
        section[data-testid="stSidebar"] div[data-testid="stSidebarUserContent"] {
            padding-top: 240px !important;
            padding-bottom: 160px !important;
        }

        /* Ocultar el separador nativo */
        section[data-testid="stSidebar"] hr {
            display: none;
        }

        /* CONTENEDOR FIJO SUPERIOR (Logo y Títulos) */
        .sidebar-top-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: var(--secondary-background-color, #262730); /* Fondo nativo de la barra */
            z-index: 999;
            padding-top: 3.5rem; /* Margen para no chocar con el botón de cerrar '<<' */
            padding-bottom: 1rem;
            box-sizing: border-box;
            border-bottom: 1px solid rgba(150, 150, 150, 0.2);
        }

        /* CONTENEDOR FIJO INFERIOR EN LA BARRA LATERAL */
        .sidebar-bottom-container {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: var(--secondary-background-color, #262730); /* Fondo nativo de la barra */
            padding: 12px 14px 10px 14px;
            z-index: 999;
            box-sizing: border-box;
            border-top: 1px solid rgba(150, 150, 150, 0.2);
        }

        /* Estilo idéntico a st.info nativo (Azul estándar) */
        .tip-card {
            background-color: rgba(28, 131, 225, 0.1);
            border: 1px solid rgba(28, 131, 225, 0.25);
            border-radius: 8px;
            padding: 10px 12px;
            font-size: 0.82rem;
            line-height: 1.35;
            margin-bottom: 12px;
        }

        /* Estilo nativo para el pie de página */
        .footer-text {
            text-align: center;
            font-size: 0.85rem;
            opacity: 0.7;
            margin: 0;
        }
        
        /* Color de la barra de pregunta del usuario */
        div[data-testid="stChatMessage"]:has(img[src*="5024235"]) {
            background-color: rgba(255, 75, 75, 0.15) !important;
            border: 2px solid #FF4B4B !important;
            border-radius: 10px !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # PLUS DE INTERFAZ: Barra Lateral de información
    with st.sidebar:
        # CONTENEDOR SUPERIOR FIJO
        st.markdown(
            """
            <div class="sidebar-top-container">
                <div style="text-align: center; margin-bottom: 2px;">
                    <img src="https://cdn-icons-png.flaticon.com/512/2412/2412042.png" width="130">
                </div>
                <h3 style='text-align: center; margin-top: 0px; margin-bottom: 0px; font-size: 1.25rem;'>Mercado Central 24h</h3>
                <p style='text-align: center; margin-bottom: 4px; font-size: 0.85rem; opacity: 0.7;'>🏢 Asistente Corporativo de IA</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # DESPLEGABLE DE DOCUMENTOS
        with st.expander("📁 Documentos Oficiales", expanded=False):
            if os.path.exists("datos"):
                pdf_files = sorted([f for f in os.listdir("datos") if f.endswith(".pdf")])
                if pdf_files:
                    for file in pdf_files:
                        if st.button(f"📄 {file}", key=f"btn_{file}", use_container_width=True):
                            mostrar_pdf(os.path.join("datos", file))
                else:
                    st.caption("No hay archivos PDF disponibles.")
            else:
                st.warning("Carpeta 'datos' no encontrada.")

        # CONTENEDOR INFERIOR FIJO
        st.markdown(
            """
            <div class="sidebar-bottom-container">
                <div class="tip-card">
                    💡 <strong>Tip de uso:</strong> Puedes preguntarme sobre manuales, políticas de la empresa, horarios, reglamentos internos y más.
                </div>
                <div class="footer-text">
                    Desarrollado con ❤️ usando <b>Streamlit</b> y <b>LangChain</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Encabezado principal
    URL_ENCABEZADO = "https://cdn-icons-png.flaticon.com/512/3082/3082011.png"
    col1, col2 = st.columns([1, 6], vertical_alignment="center")

    with col1:
        st.image(URL_ENCABEZADO, width=93)

    with col2:
        st.title("Asistente Mercado Central 24h")
        st.markdown("Bienvenido a la plataforma de consulta inteligente. Escribe tu pregunta en la caja de abajo.")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "¡Hola! Soy el agente de IA de Mercado Central 24h. Hazme preguntas sobre las políticas, operaciones y servicios.\n"
            }
        ]

    with st.spinner("Cargando base de conocimiento..."):
        try:
            vector_store, llm = initialize_system()
        except Exception as error:
            st.error(f"Ocurrió un error al cargar el sistema: {error}")
            st.stop()

    # Renderiza los mensajes guardados con avatares visuales
    URL_AVATAR_BOT = "https://cdn-icons-png.flaticon.com/512/5828/5828596.png"
    URL_AVATAR_USER = "https://cdn-icons-png.flaticon.com/512/5024/5024235.png"

    for message in st.session_state.messages:
        avatar_icon = URL_AVATAR_BOT if message["role"] == "assistant" else URL_AVATAR_USER
        with st.chat_message(message["role"], avatar=avatar_icon):
            st.markdown(message["content"])

    # Entrada de texto usando el componente de chat
    if prompt := st.chat_input("Ej: ¿Cuál es la política de devoluciones?"):
        # 1. Guarda y muestra el mensaje del usuario
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=URL_AVATAR_USER):
            st.markdown(prompt)

        # 2. Formatea el historial para LangChain
        chat_history = []
        for msg in st.session_state.messages[1:-1]:
            role_langchain = "human" if msg["role"] == "user" else "ai"
            chat_history.append((role_langchain, msg["content"]))

        # 3. Genera y muestra la respuesta de la IA
        with st.chat_message("assistant", avatar=URL_AVATAR_BOT):
            with st.spinner("Buscando en los documentos de la compañía..."):
                try:
                    # AHORA RECIBIMOS EL TEXTO Y LOS DOCUMENTOS
                    respuesta_texto, docs = generate_answer(
                        query=prompt,
                        vector_store=vector_store,
                        llm=llm,
                        chat_history=chat_history
                    )
                    
                    # AGREGA CITAS Y ENLACES AL FINAL DE LA RESPUESTA
                    respuesta_final = respuesta_texto

                    if docs:
                        respuesta_final += "\n\n---\n**📚 Fuentes consultadas:**\n"
                        fuentes_vistas = set()
                        for doc in docs:
                            doc_name = doc.metadata.get('source', 'Desconocido')
                            doc_page = doc.metadata.get('page', '?')
                            clave_unica = f"{doc_name}_{doc_page}"
                            
                            if clave_unica not in fuentes_vistas:
                                fuentes_vistas.add(clave_unica)
                                # Mostramos el archivo
                                respuesta_final += f"- 📄 **{doc_name}** (Pág. {doc_page})\n"

                    # Mostramos la respuesta con las citas integradas
                    st.markdown(respuesta_final)
                    
                    # 4. Guarda la respuesta completa en el historial
                    st.session_state.messages.append({"role": "assistant", "content": respuesta_final})
                    
                except Exception as error:
                    st.error(f"Error al generar la respuesta: {error}")

if __name__ == "__main__":
    main()