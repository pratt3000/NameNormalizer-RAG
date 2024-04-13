from src.embedder import vectorizer
from src.create_index import get_index
from src.constants import INDEX_NAME, NAMESPACE
from src.create_index import initialize_default_index


def process_query(query_str: str, top_k: int = 1, threshold: float = 0.5):
    
    # Generate embeddings for the input query.
    embeddings = vectorizer(query_str)

    # Get index object and query the pinecone vectorDB.
    merchant_index = get_index("merchant-index")
    res = merchant_index.query(vector=embeddings, top_k=top_k, include_metadata=True, namespace=NAMESPACE)

    # TODO: Add handling incase we make topk > 1 later.
    # Store the query to database if no match found.
    highest_score = res['matches'][0]['score']
    if highest_score < threshold:
        store_in_database(query_str)
        return "No match found"
    
    return res


def store_in_database(query_str: str):
    print(f"No result found. Storing {query_str} in database")


def initialize_index():
    initialize_default_index(INDEX_NAME, NAMESPACE, 'data/default_data.json')