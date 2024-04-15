import json
from dotenv import load_dotenv
import os
from uuid import uuid4
from src.model import chunk_by_size, vectorizer
from qdrant_client import QdrantClient, models


# Load environment variables from .env file
load_dotenv()
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")
QDRANT_CLOUD = os.environ.get("QDRANT_CLOUD")

qdrant_client = QdrantClient(
    QDRANT_CLOUD,
    api_key=QDRANT_API_KEY,
)

# create new collection if it doesn't already exist.
def init_collection(collection_name: str, embedding_size: int):

    if collection_name not in [n.name for n in tuple(qdrant_client.get_collections())[0][1]]:

        qdrant_client.recreate_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=embedding_size,  # Vector size is defined by used model
                distance=models.Distance.EUCLID,
            ),
        )

def get_dataobj_list(text_list: list, company_name: str) -> list:
    data_objs = [
        models.PointStruct(
            id=str(uuid4()),
            vector=vectorizer(text),
            payload={
                "company_name": company_name,
                "chunk_num": idx,
                "text_content": text,  # there are 248 chars in this chunk of text
            }
        )
        for idx, text in enumerate(text_list)
    ]

    return data_objs



def get_embeddings(text: str, company_name: str) -> list:
    """
    Given a test string, split text data into chunks, extract metadata, create embeddings for each chunk.

    :param text: Text we'd like to get embeddings for.
    :return: List of embeddings.
    """
    data_objs = []

    # Create chunks
    chunked_text = chunk_by_size(text)

    # Extract just the string content from the chunk
    chunked_text = [c.page_content for c in chunked_text]

    # Extract some metadata, create an ID, and generate an embedding for the chunk.
    data_objs = get_dataobj_list(chunked_text, company_name)

    return data_objs


def initialize_default_collection(collection_name, dummy_data, embedding_size):
    # Create a new index
    init_collection(collection_name, embedding_size)

    # Insert embeddings into Qdrant
    for company_name in dummy_data.keys():
        data_objs = get_dataobj_list(dummy_data[company_name], company_name)
        upload_objlist_to_Qdrant(collection_name, data_objs)

    # Print index stats
    print(qdrant_client.get_collection(collection_name=collection_name))


def upload_objlist_to_Qdrant(collection_name: str, data_objs: list):
    qdrant_client.upload_points(
        collection_name=collection_name,
        points = data_objs,
    )

def search_qdrant(collection_name: str, query: str, limit: int = 1):
    hits = qdrant_client.search(
        collection_name=collection_name,
        query_vector=vectorizer(query),
        limit=limit,
    )

    return hits

    