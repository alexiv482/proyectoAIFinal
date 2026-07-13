"""Utilidades para cargar los documentos fuente del proyecto."""

from pathlib import Path

import pymupdf
from langchain_core.documents import Document


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
