"""Punto de entrada principal para la aplicación del agente."""

from helpers import load_pdf_documents, split_documents, create_vector_index, search_documents
from models import create_embeddings

def main() -> None:
    """Ejecuta el flujo de preparación de documentos y prueba el sistema de búsqueda."""
    try:
        print("1. Cargando documentos PDF desde el directorio local...")
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
        print("   -> Índice vectorial creado con éxito.")

        print("\n5. Probando el sistema de búsqueda semántica...")
        #cambiar este texto por algo que exista en tu PDF de prueba
        query_test = "Mercado Central" 
        print(f"   -> Consulta de prueba: '{query_test}'")
        
        results = search_documents(query_test, vector_store)
        
        if results:
            print(f"   -> Se encontraron {len(results)} fragmentos relevantes:\n")
            for i, res in enumerate(results, start=1):
                origen = res.metadata.get("source", "Desconocido")
                pagina = res.metadata.get("page", "?")
                # Mostramos los primeros 100 caracteres de cada resultado
                print(f"      [{i}] {origen} (Pág. {pagina}): {res.page_content[:100]}...")
        else:
            print("   -> No se encontraron resultados relevantes.")

    except Exception as error:
        print(f"Error durante la ejecución del pipeline: {error}")

if __name__ == "__main__":
    main()