from src.model import vectorizer
from src.constants import INDEX_NAME, NAMESPACE, DUMMY_DATA_PATH
from src.pinecone_utils import initialize_default_index, get_index
from db.crud import create_db_query

from sqlalchemy.orm import Session


def process_query(
    db_session: Session, query_str: str, top_k: int = 1, threshold: float = 0.5
):
    # Generate embeddings for the input query.
    embeddings = vectorizer(query_str)

    # Get index object and query the pinecone vectorDB.
    merchant_index = get_index("merchant-index")
    res = merchant_index.query(
        vector=embeddings, top_k=top_k, include_metadata=True, namespace=NAMESPACE
    )

    # TODO: Add handling incase we make topk > 1 later.
    # Store the query to database if no match found.
    highest_score = res["matches"][0]["score"]
    if highest_score < threshold:
        create_db_query(db_session, query_str)
        return "No match found"

    return res


def initialize_index():
    initialize_default_index(INDEX_NAME, NAMESPACE, DUMMY_DATA_PATH)
