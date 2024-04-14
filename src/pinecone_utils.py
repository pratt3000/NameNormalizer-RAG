from pinecone import Pinecone, ServerlessSpec
import json
from src.constants import EMBEDDINGS_SIZE
from dotenv import load_dotenv
import os
from uuid import uuid4
from src.model import chunk_by_size, vectorizer

# Load environment variables from .env file
load_dotenv()
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")

pc = Pinecone(api_key=PINECONE_API_KEY)


def init_index(index_name: str):
    if index_name in pc.list_indexes().names():
        pc.delete_index(index_name)

    pc.create_index(
        name=index_name,
        dimension=EMBEDDINGS_SIZE,  # Replace with your model dimensions
        metric="euclidean",  # Replace with your model metric
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )


def get_index(index_name: str):
    index = pc.Index(index_name)
    return index


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
    # Wrap that all in a dictionary.
    for idx, text in enumerate(chunked_text):
        payload = {
            "metadata": {
                "company_name": company_name,
                "chunk_num": idx,
                "text_content": text,  # there are 248 chars in this chunk of text
            },
            "id": str(uuid4()),
            "values": vectorizer(text),
        }
        data_objs.append(payload)
    return data_objs


def initialize_default_index(index_name, namespace, data_file_path):
    # Create a new index
    init_index(index_name)
    merchant_index = get_index(index_name)

    # read json file
    with open(data_file_path) as f:
        data = json.load(f)

    # Insert embeddings into Pinecone
    for company in data.keys():
        for alternative_name in data[company]:
            embeddings = get_embeddings(
                alternative_name, company
            )  # Get embeddings for each alternative name
            merchant_index.upsert(
                vectors=embeddings, namespace=namespace
            )  # Insert embeddings batch into Pinecone

    # Print index stats
    print(merchant_index.describe_index_stats())
