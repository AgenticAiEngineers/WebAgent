import chromadb
from sentence_transformers import SentenceTransformer

class VectorMemory:

    def __init__(self):
        # Load embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # Initialize ChromaDB client
        self.client = chromadb.Client()

        # Create or get collection
        self.collection = self.client.get_or_create_collection(name="chat_memory")

    def store_memory(self, text, id):
        """
        Convert text to embedding and store in vector DB
        """
        embedding = self.model.encode(text).tolist()

        self.collection.add(
            documents=[text],
            embeddings=[embedding],
            ids=[str(id)]
        )

    def search_memory(self, query, top_k=3):
        """
        Search similar memories using semantic similarity
        """
        query_embedding = self.model.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results["documents"][0] if results["documents"] else []
