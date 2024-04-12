from pinecone import Pinecone, ServerlessSpec
import json
from src.embedder import get_embeddings
from src.constants import PINECONE_API_KEY, EMBEDDINGS_SIZE

pc = Pinecone(api_key=PINECONE_API_KEY)


def init_index(index_name: str):

    if index_name in pc.list_indexes().names():
        pc.delete_index(index_name)

    pc.create_index(
        name=index_name,
        dimension=EMBEDDINGS_SIZE,     # Replace with your model dimensions
        metric="euclidean", # Replace with your model metric
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        ) 
    )


def get_index(index_name: str):
    index = pc.Index(index_name)
    return index


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

            embeddings = get_embeddings(alternative_name, company)  # Get embeddings for each alternative name
            merchant_index.upsert(vectors=embeddings, namespace=namespace)      # Insert embeddings batch into Pinecone 

    # Print index stats
    print(merchant_index.describe_index_stats())