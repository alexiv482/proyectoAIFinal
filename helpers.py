"""Utilidades para cargar los documentos fuente del proyecto."""

from pathlib import Path

import pymupdf
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_core.embeddings import Embeddings#
from langchain_core.vectorstores import InMemoryVectorStore, VectorStore#

DEFAULT_CHUNK_SIZE = 500
DEFAULT_CHUNK_OVERLAP = 50


class DocumentLoadError(Exception):
    """Indica que no fue posible cargar los documentos fuente."""


def load_pdf_documents(documents_directory: str | Path = "datos") -> list[Document]:
    """Carga todos los PDF de un directorio como documentos de LangChain."""
    directory = Path(documents_directory)
    _validate_documents_directory(directory)

    pdf_paths = sorted(directory.glob("*.pdf"))
    if not pdf_paths:
        raise DocumentLoadError(
            f"No se encontraron archivos PDF en: {directory.resolve()}"
        )

    documents = [
        document
        for pdf_path in pdf_paths
        for document in _load_pdf_pages(pdf_path)
    ]
    if not documents:
        raise DocumentLoadError("Los PDF encontrados no contienen texto extraíble.")

    return documents


def split_documents(
    documents: list[Document],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[Document]:
    """Fragmenta documentos y conserva sus metadatos."""
    if not documents:
        raise ValueError("Se requiere al menos un documento para fragmentar.")
    if chunk_size <= 0:
        raise ValueError("El tamaño de fragmento debe ser mayor que cero.")
    if not 0 <= chunk_overlap < chunk_size:
        raise ValueError("El solapamiento debe ser menor que el tamaño de fragmento.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_documents(documents)


def _validate_documents_directory(directory: Path) -> None:
    """Verifica que el directorio de documentos exista y sea válido."""
    if not directory.exists():
        raise DocumentLoadError(f"No existe el directorio: {directory.resolve()}")
    if not directory.is_dir():
        raise DocumentLoadError(f"La ruta no es un directorio: {directory.resolve()}")


def _load_pdf_pages(pdf_path: Path) -> list[Document]:
    """Extrae una lista de documentos, uno por página con texto, de un PDF."""
    try:
        with pymupdf.open(pdf_path) as pdf:
            return [
                Document(
                    page_content=page_text,
                    metadata={
                        "source": pdf_path.name,
                        "page": page_number,
                    },
                )
                for page_number, page in enumerate(pdf, start=1)
                if (page_text := page.get_text("text").strip())
            ]
    except (OSError, RuntimeError) as error:
        raise DocumentLoadError(
            f"No fue posible leer el PDF '{pdf_path.name}'."
        ) from error


def create_vector_index(documents: list[Document], embeddings_model: Embeddings) -> InMemoryVectorStore:
    """Crea un índice vectorial en memoria a partir de los fragmentos y el modelo de embeddings."""
    if not documents:
        raise ValueError("La lista de fragmentos de documentos está vacía.")
    if not embeddings_model:
        raise ValueError("Se requiere un modelo de embeddings válido.")

    return InMemoryVectorStore.from_documents(
        documents=documents,
        embedding=embeddings_model,
    )

def search_documents(query: str, vector_store: VectorStore, k: int = 4) -> list[Document]:
    """Realiza una búsqueda de similitud en el índice vectorial devolviendo los k fragmentos más relevantes."""
    if not query.strip():
        raise ValueError("La consulta de búsqueda no puede estar vacía.")
    if not vector_store:
        raise ValueError("Se requiere un índice vectorial válido para buscar.")
        
    # similarity_search devuelve los documentos más cercanos al query en el espacio vectorial
    return vector_store.similarity_search(query, k=k)