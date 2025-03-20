# import chromadb
# import uuid
# import shutil
# import os
# from utils import get_embedding

# db_path = "./chroma_db"
# if os.path.exists(db_path):

#     shutil.rmtree(db_path)
#     print(f"Existing database at '{db_path}' has been deleted.")
# client = chromadb.PersistentClient(path=db_path)
# collection = client.get_or_create_collection("code_snippets")

# def add_to_db(embedding, metadata):
#     new_id = str(uuid.uuid4())
#     collection.add(ids=[new_id], embeddings=[embedding], metadatas=[metadata])

# def search_code(query, k=8):
#     """Search DB for similar chunks & return metadata
#   query: search query
#   k: number of chunks to return
#    """

#     query_embedding = get_embedding(query)
#     results = collection.query(query_embeddings=[query_embedding], n_results=k)
#     results = results.get("metadatas", [[]])[0]

#     if not results:
#         return "No relevant code found."

#     extracted_code = "\n\n".join(
#         f"File: {res['file_path']}\nCode:\n{res['chunk_text']}"
#         for res in results)

#     return extracted_code

import faiss
import numpy as np
from utils.utils import get_embedding

# Configuration
dim = 768  # Adjust to match your embedding size

# Initialize FAISS index and metadata
index = faiss.IndexFlatL2(dim)
metadata = []

def add_to_db(embedding, metadata_entry):
    embedding = np.array(embedding, dtype=np.float32).reshape(1, -1)
    index.add(embedding)
    metadata.append(metadata_entry)  # Maintain order with embeddings

def search_code(query, k=10):
    """Search DB for similar chunks & return metadata
    query: search query
    k: number of chunks to return
    """
    if index.ntotal == 0:
        return "No relevant code found."

    query_embedding = np.array(get_embedding(query), dtype=np.float32).reshape(1, -1)
    _, indices = index.search(query_embedding, k)

    results = [metadata[idx] for idx in indices[0] if idx != -1]

    if not results:
        return "No relevant code found."

    extracted_code = "\n\n".join(
        f"File: {res['file_path']}\nCode:\n{res['chunk_text']}" for res in results
    )

    return extracted_code

