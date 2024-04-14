from sqlalchemy.orm import Session
from db import models
from typing import List


def create_db_query(db_session: Session, query_str: str):
    db_query = models.Query(query=query_str)

    db_session.add(db_query)
    db_session.commit()
    db_session.refresh(db_query)
    return db_query


def get_table_data(db_session: Session):
    return db_session.query(models.Query).filter(models.Query.is_active == True).all()


def update_query_status(db_session: Session, query_ids: List[int], status: bool):
    for query_id in query_ids:
        db_query = db_session.query(models.Query).filter(models.Query.id == query_id).first()
        db_query.is_active = status
        db_session.flush()
    db_session.commit()