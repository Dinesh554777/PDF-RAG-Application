from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import os

class QdrantStorage:
    def __init__(self, url=None, collection="docs_v2",dim=384):
        # Use environment variable if available, otherwise use default
        if url is None:
            url = os.getenv("QDRANT_URL", "http://localhost:6333")
        self.client = QdrantClient(url=url, timeout=30)
        self.collection = collection
        if not self.client.collection_exists(self.collection):
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
                )

    def clear(self):
        self.client.delete_collection(collection_name=self.collection)
        self.client.create_collection(
            collection_name=self.collection,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )

    def upsert(self, ids, vectors, payloads):
        point = [PointStruct(id=ids[i], vector=vectors[i], payload=payloads[i]) for i in range(len(ids))]
        self.client.upsert(self.collection, points=point) 

    def search(self, query_vector, top_k=5):
        results = self.client.query_points(
            collection_name=self.collection,
            query=query_vector,
            with_payload=True,
            limit=top_k
        ).points
        contexts = []
        sources = []

        for r in results:
            payload=getattr(r, 'payload', None) or {}
            text=payload.get('text', "")
            source=payload.get('source', "")
            
            if text:
                contexts.append(text)
                sources.append(source)

        return {"contexts": contexts, "sources": list(sources)}