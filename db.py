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

# import faiss
# import numpy as np
# from utils.utils import get_embedding

# # Configuration
# dim = 768  # Adjust to match your embedding size

# # Initialize FAISS index and metadata
# index = faiss.IndexFlatL2(dim)
# metadata = []

# def add_to_db(embedding, metadata_entry):
#     embedding = np.array(embedding, dtype=np.float32).reshape(1, -1)
#     index.add(embedding)
#     metadata.append(metadata_entry)  # Maintain order with embeddings

# def search_code(query, k=10):
#     """Search DB for similar chunks & return metadata
#     query: search query
#     k: number of chunks to return
#     """
#     if index.ntotal == 0:
#         return "No relevant code found."

#     query_embedding = np.array(get_embedding(query), dtype=np.float32).reshape(1, -1)
#     _, indices = index.search(query_embedding, k)

#     results = [metadata[idx] for idx in indices[0] if idx != -1]

#     if not results:
#         return "No relevant code found."

#     extracted_code = "\n\n".join(
#         f"File: {res['file_path']}\nCode:\n{res['chunk_text']}" for res in results
#     )

#     return extracted_code





import os
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from utils.utils import parse_agent_response
import google.generativeai as genai
from langchain.embeddings.base import Embeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.retrievers.multi_query import MultiQueryRetriever
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
 
class GeminiEmbeddings(Embeddings):
    """Custom Gemini embeddings wrapper for LangChain."""

    def embed_query(self, text: str):
        """Generate embeddings for a single query."""
        response = genai.embed_content(model="models/embedding-001",
                                   content=text,
                                   task_type="retrieval_document")
        return response["embedding"]  # Return the embedding vector

    def embed_documents(self, texts):
        """Generate embeddings for multiple documents."""
        
        responses = [self.embed_query(text) for text in texts]
        return responses  # List of embedding vectors


INDEX_PATH = "faiss_index"
# if os.path.exists(INDEX_PATH):
#     vector_store = FAISS.load_local(INDEX_PATH, embeddings)
# else:
embeddings = GeminiEmbeddings()
llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash", temperature=0.3)

vector_store = FAISS.from_documents([Document(page_content="Ireelevant", metadata={"file_path":"None"})], embeddings)


retriever = MultiQueryRetriever.from_llm(retriever=vector_store.as_retriever(), llm=llm)

retrieval_chain = RetrievalQA.from_chain_type(llm, retriever=retriever)


def add_to_db(page_content, metadata_entry):
    """Adds a new document to FAISS and saves it persistently."""
    global vector_store

    doc = Document(page_content=page_content, metadata=metadata_entry)

    
    vector_store.add_documents([doc])

    # vector_store.save_local(INDEX_PATH)



def search_code(response):
    """Search FAISS index for similar code snippets and return as documents."""
    params = parse_agent_response(response)
    query = params.get("query","")
    k= int(params.get("k","10"))
    if vector_store is None:
        return []

    results = vector_store.similarity_search(query, k)

    return results  # Return list of Document objects
