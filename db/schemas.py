from pydantic import BaseModel


# Schema for the queries table.
class Queries(BaseModel):
    query: str
    is_active: bool = True
