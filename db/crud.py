from sqlalchemy.orm import Session
from db import schemas, models
from db.schemas import Queries


def create_db_query(db_session: Session, query_str: str):
    db_query = models.Query(query=query_str)

    db_session.add(db_query)
    db_session.commit()
    db_session.refresh(db_query)
    return db_query
