from db.database import Base
from sqlalchemy import Column, Integer, String, Boolean


# Define the schema for the queries table.
class Query(Base):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, index=True)
    is_active = Column(Boolean, default=True)
