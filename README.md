# 🛒 Asistente Mercado Central 24h - Agente de IA

## 📝 Descripción General
Este proyecto es un agente de Inteligencia Artificial diseñado para Mercado Central 24h. Su propósito es ayudar a las personas colaboradoras a encontrar información rápidamente dentro de los documentos internos de la empresa (manuales, políticas, etc.) mediante preguntas en lenguaje natural, evitando que pierdan horas buscando datos en archivos extensos.

## 🏗️ Arquitectura de la Solución
El sistema utiliza un enfoque RAG (Retrieval-Augmented Generation) que consta de las siguientes etapas:
1. **Carga y Fragmentación:** Se procesan documentos PDF locales extrayendo su texto y dividiéndolo en fragmentos semánticos usando `langchain`.
2. **Embeddings e Índice Vectorial:** Se generan representaciones vectoriales del texto utilizando el modelo de Cohere y se almacenan en un índice en memoria (`InMemoryVectorStore`).
3. **Recuperación (Retrieval):** Ante una consulta del usuario, el sistema busca los fragmentos de texto más relevantes en la base vectorial.
4. **Generación:** Se envía el contexto recuperado junto con el historial de la conversación a un modelo de lenguaje (LLM) de Groq (`llama-3.3-70b-versatile`) para generar una respuesta precisa y fundamentada exclusivamente en los documentos.
5. **Interfaz de Usuario:** Una aplicación web interactiva desarrollada con Streamlit que mantiene el estado de la sesión y el historial de chat.

## 🛠️ Tecnologías y Herramientas Utilizadas
* **Lenguaje:** Python 3.13
* **Framework IA:** LangChain
* **Interfaz Gráfica:** Streamlit
* **Embeddings:** Cohere (`embed-v4.0`)
* **Modelo de Lenguaje (LLM):** Groq (`llama-3.3-70b-versatile`)
* **Procesamiento de PDF:** PyMuPDF
* **Despliegue:** Oracle Cloud Infrastructure (OCI)

## 🚀 Instrucciones para Ejecutar el Proyecto (Local)

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/alexiv482/proyectoAIFinal.git
   cd "proyectoAIFinal"