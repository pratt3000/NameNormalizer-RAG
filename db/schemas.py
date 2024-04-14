from pydantic import BaseModel


class Queries(BaseModel):
    query: str
    is_active: bool = True
