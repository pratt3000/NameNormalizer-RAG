from pydantic import BaseModel


class Queries(BaseModel):
    query: str
