from fastapi import FastAPI
from pydantic import BaseModel
import openai
import numpy as np
import faiss

app = FastAPI()

# Saving my own free API key which we can get from OPENAI platform.
openai.api_key = "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"


class QueryRequest(BaseModel):
    query: str


# Mock data for retrieval, can be replaced with real data
documents = [
    "Document 1: FastAPI is a modern, fast web framework for building APIs.",
    "Document 2: Retrieval-Augmented Generation (RAG) combines information retrieval with natural language generation.",
    "Document 3: Faiss is a library for efficient similarity search and clustering of dense vectors.",
]


# Vectorize documents (using embeddings)
def get_embeddings(texts):
    return [np.random.rand(512) for _ in texts]  # Replace with real embeddings


# I am using faiss index for information retrival
def build_faiss_index(embeddings):
    dim = 512
    index = faiss.IndexFlatL2(dim)  # L2 distance
    index.add(np.array(embeddings))
    return index


# Precomputeing  document embeddings and index
doc_embeddings = get_embeddings(documents)
faiss_index = build_faiss_index(doc_embeddings)


# Retrieveing documents  based on a query
def retrieve_documents(query_embedding):
    D, I = faiss_index.search(np.array([query_embedding]), k=2)  # Retrieve top-2 docs
    return [documents[i] for i in I[0]]


# Generating a response using retrieved docs from faiss index
def generate_response(query, retrieved_docs):
    context = " ".join(retrieved_docs)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use a model like gpt-3.5-turbo or gpt-4
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Query: {query}\nContext: {context}\nAnswer:"}
        ],
        max_tokens=100
    )
    return response['choices'][0]['message']['content'].strip()


@app.post("/query")
def handle_query(request: QueryRequest):
    # Mock embedding
    
    query_embedding = np.random.rand(512)

    # Retrieving other  relevant documents
    retrieved_docs = retrieve_documents(query_embedding)

    # Generating  a response
    response = generate_response(request.query, retrieved_docs)

    return {"query": request.query, "response": response, "documents": retrieved_docs}
