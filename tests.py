from src.constants import COLLECTION_NAME, EMBEDDINGS_SIZE
from dotenv import load_dotenv
import os
from src.qdrant_utils import initialize_default_collection
from qdrant_client import QdrantClient
from src.scheduler import scrape_data_and_upload_embeddings_to_qdrant

load_dotenv()
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")
QDRANT_CLOUD = os.environ.get("QDRANT_CLOUD")

qdrant_client = QdrantClient(
    QDRANT_CLOUD,
    api_key=QDRANT_API_KEY,
)


# Test the dummy data injection
def test_dummy_data_injection():
    dummy_data = {
        "Apple": ["Apple Inc.", "Iphone", "Ipad", "Macbook"],
        "Google": ["Google Inc.", "Google Android"],
        "Microsoft": ["Microsoft Corporation", "MSFT Windows", "Microsoft Office"],
    }

    try:
        initialize_default_collection(COLLECTION_NAME, dummy_data, EMBEDDINGS_SIZE)
    except Exception as e:
        print(f"Error: {e}")


# Test the data scraper and embedding injection
def test_data_scraper_and_embedding_injection():
    try:
        table_names = ["msft", "google"]

        scrape_data_and_upload_embeddings_to_qdrant(table_names)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # TODO: Write better/segregated tests. Didnt get time to finish the bonus entirely part.

    test_dummy_data_injection()
    test_data_scraper_and_embedding_injection()
