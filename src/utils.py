from src.qdrant_utils import search_qdrant
from db.crud import create_db_query

from sqlalchemy.orm import Session

def process_query(
    db_session: Session, collection_name: str, query_str: str, top_k: int = 1, threshold: float = 0.5
):
    
    # Get closest vector from Qdrant database.
    res = search_qdrant(collection_name, query_str, limit=top_k)

    # TODO: Add handling incase we make topk > 1 later.
    # Store the query to database if no match found.
    eucledian_distance = res[0].score
    if eucledian_distance > threshold:
        create_db_query(db_session, query_str)
        return "No match found"
    
    ans = {
        "normalized company name": res[0].payload['company_name'],
        "eucledian distance": eucledian_distance,
        'vector_text': res[0].payload['text_content']
    }

    return ans

