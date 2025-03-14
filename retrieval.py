from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class RAGRetriever:
    def __init__(self):
        self.documents = [
            "Stable Diffusion is a text-to-image model.",
            "RAG combines retrieval with language generation.",
            "FAISS is used for similarity search in dense vector spaces.",
            "Flan-T5 is a fine-tuned LLM used for text generation."
        ]
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        doc_embeddings = self.embedder.encode(self.documents)
        self.index = faiss.IndexFlatL2(doc_embeddings.shape[1])
        self.index.add(np.array(doc_embeddings))

    def retrieve(self, query, top_k=2):
        query_emb = self.embedder.encode([query])
        D, I = self.index.search(np.array(query_emb), top_k)
        return [self.documents[i] for i in I[0]]

if __name__ == "__main__":
    retriever = RAGRetriever()
    print("Retrieved Documents:", retriever.retrieve("What is RAG?"))
