from src.embedder import vectorizer
from src.create_index import get_index
from src.constants import INDEX_NAME, NAMESPACE
from src.create_index import initialize_default_index


def get_topk_matches(query_str: str, top_k: int = 1):
    
    embeddings = vectorizer(query_str)

    merchant_index = get_index("merchant-index")
    res = merchant_index.query(vector=embeddings, top_k=top_k, include_metadata=True, namespace=NAMESPACE)
    
    return res

def initialize_index():
    initialize_default_index(INDEX_NAME, NAMESPACE, 'data/default_data.json')