"""Punto de entrada principal para la aplicación del agente."""

from helpers import load_pdf_documents, split_documents, create_vector_index
from models import create_embeddings

def main() -> None:
    """Ejecuta el flujo de preparación de documentos y creación del índice vectorial."""
    try:
        print("1. Cargando documentos PDF desde el directorio local...")
        # Nota: Asegúrate de tener un archivo PDF dentro de la carpeta 'datos'
        docs = load_pdf_documents("datos")
        print(f"   -> Se extrajeron {len(docs)} páginas con texto.")

        print("\n2. Fragmentando documentos...")
        chunks = split_documents(docs)
        print(f"   -> Se generaron {len(chunks)} fragmentos de texto.")

        print("\n3. Cargando modelo de embeddings de Cohere...")
        embeddings = create_embeddings()
        print("   -> Modelo de embeddings configurado exitosamente.")

        print("\n4. Generando embeddings y creando el índice vectorial en memoria...")
        vector_store = create_vector_index(chunks, embeddings)
        print("   -> Índice vectorial creado con éxito y listo para realizar búsquedas.")

    except Exception as error:
        print(f"Error durante la ejecución del pipeline: {error}")

if __name__ == "__main__":
    main()