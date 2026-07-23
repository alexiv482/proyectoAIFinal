"""Punto de entrada principal para la aplicación del agente."""

from helpers import (
    create_vector_index,
    generate_answer,
    load_pdf_documents,
    split_documents,
)
from models import create_embeddings, create_llm

def main() -> None:
    """Ejecuta el pipeline RAG generando respuestas asistidas por contexto."""
    try:
        print("1. Cargando documentos PDF desde el directorio local...")
        docs = load_pdf_documents("datos")
        print(f"   -> Se extrajeron {len(docs)} páginas con texto.")

        print("\n2. Fragmentando documentos...")
        chunks = split_documents(docs)
        print(f"   -> Se generaron {len(chunks)} fragmentos de texto.")

        print("\n3. Configurando modelo de embeddings y LLM...")
        embeddings = create_embeddings()
        llm = create_llm()
        print("   -> Modelos inicializados exitosamente.")

        print("\n4. Generando índice vectorial en memoria...")
        vector_store = create_vector_index(chunks, embeddings)
        print("   -> Índice listo.")

        print("\n5. Generando respuesta con contexto del documento...")
        query = "¿Qué es Mercado Central 24h y dónde tiene presencia?"
        print(f"   Pregunta: {query}\n")

        respuesta = generate_answer(query, vector_store, llm)
        print("   Respuesta del Agente:")
        print("   " + "-" * 50)
        print(respuesta)
        print("   " + "-" * 50)

    except Exception as error:
        print(f"Error durante la ejecución: {error}")


if __name__ == "__main__":
    main()