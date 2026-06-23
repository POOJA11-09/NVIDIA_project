from rag.query import QueryEngine
 
 
class Retriever:
 
    def __init__(self):
        self.engine = QueryEngine()
 
    def retrieve(self, query, k=8):
 
        results = self.engine.search(query, top_k=k)
 
        return results