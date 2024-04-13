from db.database import Base
from sqlalchemy import Column, Integer, String

class Query(Base):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, index=True)