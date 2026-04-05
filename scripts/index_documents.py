#!/usr/bin/env python3
# scripts/index_documents.py — Indexation FAISS des documents juridiques CarthagoLex
"""
Usage:
    python scripts/index_documents.py --docs_dir data/docs --index_dir data/faiss_index

Formats supportes : .txt, .pdf, .md
"""
import os
import sys
import argparse
import pickle
import json
from pathlib import Path

# Ajouter le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

import config


def load_documents(docs_dir: str):
    """Charge tous les documents du dossier donne."""
    docs = []
    docs_path = Path(docs_dir)
    if not docs_path.exists():
        print(f"Dossier introuvable : {docs_dir}")
        return docs

    for file_path in docs_path.rglob("*"):
        if file_path.suffix.lower() == ".txt":
            try:
                content = file_path.read_text(encoding="utf-8")
                docs.append({
                    "content": content,
                    "source": file_path.name,
                    "metadata": {
                        "path": str(file_path),
                        "type": "txt"
                    }
                })
                print(f"  Charge : {file_path.name}")
            except Exception as e:
                print(f"  Erreur lecture {file_path.name} : {e}")

        elif file_path.suffix.lower() == ".pdf":
            try:
                import pdfplumber
                with pdfplumber.open(file_path) as pdf:
                    text = "\n".join(
                        page.extract_text() or "" for page in pdf.pages
                    )
                docs.append({
                    "content": text,
                    "source": file_path.name,
                    "metadata": {
                        "path": str(file_path),
                        "type": "pdf"
                    }
                })
                print(f"  Charge PDF : {file_path.name}")
            except ImportError:
                print("  pdfplumber non installe - pip install pdfplumber")
            except Exception as e:
                print(f"  Erreur PDF {file_path.name} : {e}")

        elif file_path.suffix.lower() == ".md":
            try:
                content = file_path.read_text(encoding="utf-8")
                docs.append({
                    "content": content,
                    "source": file_path.name,
                    "metadata": {
                        "path": str(file_path),
                        "type": "markdown"
                    }
                })
                print(f"  Charge Markdown : {file_path.name}")
            except Exception as e:
                print(f"  Erreur lecture {file_path.name} : {e}")

    return docs


def chunk_documents(docs, chunk_size: int = 1000, overlap: int = 200):
    """Decoupe les documents en chunks avec chevauchement."""
    chunks = []
    for doc in docs:
        content = doc["content"]
        start = 0
        while start < len(content):
            end = start + chunk_size
            chunk_text = content[start:end]
            if chunk_text.strip():
                chunks.append({
                    "content": chunk_text,
                    "source": doc["source"],
                    "score": 0.0,
                    "metadata": doc.get("metadata", {})
                })
            start += chunk_size - overlap
    return chunks


def build_faiss_index(chunks, index_dir: str):
    """Construit et sauvegarde l'index FAISS."""
    try:
        import faiss
        import numpy as np
        from models.embedder import embed_documents
    except ImportError as e:
        print(f"Dependance manquante : {e}")
        print("pip install faiss-cpu openai numpy")
        sys.exit(1)

    print(f"\nGeneration des embeddings pour {len(chunks)} chunks...")
    texts = [c["content"] for c in chunks]

    embeddings = []
    for i, text in enumerate(texts):
        if i % 10 == 0:
            print(f"  Embedding {i+1}/{len(texts)}...")
        from models.embedder import embed_text
        vec = embed_text(text)
        embeddings.append(vec)

    embeddings_np = np.array(embeddings, dtype="float32")
    dimension = embeddings_np.shape[1]

    print(f"\nCreation de l'index FAISS (dimension={dimension})...")
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings_np)

    # Sauvegarde
    index_path = Path(index_dir)
    index_path.mkdir(parents=True, exist_ok=True)

    faiss.write_index(index, str(index_path / "index.faiss"))
    with open(index_path / "documents.pkl", "wb") as f:
        pickle.dump(chunks, f)

    print(f"Index sauvegarde dans : {index_dir}")
    print(f"  {index.ntotal} vecteurs indexes")
    print(f"  {len(chunks)} documents references")


def main():
    parser = argparse.ArgumentParser(
        description="Indexe les documents juridiques CarthagoLex dans FAISS"
    )
    parser.add_argument(
        "--docs_dir",
        default="data/docs",
        help="Dossier contenant les documents juridiques (.txt, .pdf, .md)"
    )
    parser.add_argument(
        "--index_dir",
        default=config.FAISS_INDEX_PATH,
        help="Dossier de destination de l'index FAISS"
    )
    parser.add_argument(
        "--chunk_size",
        type=int,
        default=1000,
        help="Taille des chunks en caracteres"
    )
    parser.add_argument(
        "--overlap",
        type=int,
        default=200,
        help="Chevauchement entre chunks"
    )
    args = parser.parse_args()

    print(f"CarthagoLex - Indexation FAISS")
    print(f"Dossier documents : {args.docs_dir}")
    print(f"Dossier index     : {args.index_dir}")
    print(f"Chunk size        : {args.chunk_size}")
    print()

    print("Chargement des documents...")
    docs = load_documents(args.docs_dir)
    if not docs:
        print("Aucun document trouve. Verifiez le dossier.")
        sys.exit(1)
    print(f"{len(docs)} documents charges.")

    print("\nDecoupage en chunks...")
    chunks = chunk_documents(docs, args.chunk_size, args.overlap)
    print(f"{len(chunks)} chunks crees.")

    print("\nConstruction de l'index FAISS...")
    build_faiss_index(chunks, args.index_dir)

    print("\nIndexation terminee avec succes !")
    print(f"Lancez maintenant : python app.py")


if __name__ == "__main__":
    main()
