from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.orm import Session
import random
import uvicorn

from src.utils import process_query
from db.schemas import Queries
from db.database import engine, SessionLocal
from db import models
from db.crud import create_db_query

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# This is the endpoint that will save the query to the database``
@app.post("/save_query/")
async def save_query(queries: Queries, db_session: Session = Depends(get_db)):
    create_db_query(db_session, queries.query)


# This is the endpoint that will return the query from the database
@app.get("/pm/{query}")
async def get_merchant(query: str = None, db_session: Session = Depends(get_db)):
    res = process_query(db_session, query, top_k=1, threshold=0.5)

    output = {"query": query, "output": str(res)}
    return output


# This is the default test endpoint
@app.get("/")
async def root(query: str = None):
    return {"message": f"Hello World {random.randint(1, 100)}"}


if __name__ == "__main__":
    uvicorn.run(app, port=8888)
