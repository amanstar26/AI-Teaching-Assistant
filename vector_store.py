from embedding_model import load_embedding_model
import faiss
import numpy as np
import traceback
import pickle
import os
import json

def create_faiss_index(chunks):

    try:

        print("Loading embedding model...")

        model = load_embedding_model()

        print("Model loaded")

        print("Creating embeddings...")

        embeddings = model.encode(
            chunks,
            convert_to_numpy=True
        )

        print("Embeddings created")

        dimension = embeddings.shape[1]

        index = faiss.IndexFlatL2(
            dimension
        )

        index.add(embeddings)

        print("FAISS index ready")

        return index, model

    except Exception as e:

        print("\nERROR OCCURRED:")
        print(e)

        traceback.print_exc()

        raise

def search_chunks(
        question,
        index,
        model,
        chunks,
        top_k=5
    ):

    print(f"\nSearching Question: {question}")

    question_embedding = model.encode(
        [question],
        convert_to_numpy=True
    )

    distances, indices = index.search(
        question_embedding,
        top_k
    )

    results = []

    for idx in indices[0]:

        if idx < len(chunks):

            results.append(
                chunks[idx]
            )

    return results

def save_index(index):

    os.makedirs(
        "vector_store",
        exist_ok=True
    )

    faiss.write_index(
        index,
        "vector_store/faiss.index"
    )

def load_index():

    return faiss.read_index(
        "vector_store/faiss.index"
    )

def save_chunks(chunks):

    with open(
        "vector_store/chunks.pkl",
        "wb"
    ) as f:

        pickle.dump(
            chunks,
            f
        )

def load_chunks():

    with open(
        "vector_store/chunks.pkl",
        "rb"
    ) as f:

        return pickle.load(f)

def save_metadata(pdf_name):

    metadata = {
        "pdf_name": pdf_name
    }

    with open(
        "vector_store/metadata.json",
        "w"
    ) as f:

        json.dump(
            metadata,
            f,
            indent=4
        )

def load_metadata():

    if not os.path.exists(
        "vector_store/metadata.json"
    ):
        return None

    with open(
        "vector_store/metadata.json",
        "r"
    ) as f:

        return json.load(f)

def is_same_pdf(pdf_name):

    metadata = load_metadata()

    if metadata is None:
        return False

    return (
        metadata.get("pdf_name")
        == pdf_name
    )

def vector_store_exists():

    return (
        os.path.exists(
            "vector_store/faiss.index"
        )
        and
        os.path.exists(
            "vector_store/chunks.pkl"
        )
        and
        os.path.exists(
            "vector_store/metadata.json"
        )
    )