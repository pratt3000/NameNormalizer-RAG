from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
import tiktoken
from src.constants import MODEL_NAME, TOKENIZER_NAME
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

embed = OpenAIEmbeddings(model=MODEL_NAME, openai_api_key=OPENAI_API_KEY)

# Tell tiktoken what model we'd like to use for embeddings
tiktoken.encoding_for_model(MODEL_NAME)

# Intialize a tiktoken tokenizer (i.e. a tool that identifies individual tokens (words))
tokenizer = tiktoken.get_encoding(TOKENIZER_NAME)


# Create our custom tiktoken function
def tiktoken_len(text: str) -> int:
    """
    Split up a body of text using a custom tokenizer.

    :param text: Text we'd like to tokenize.
    """
    tokens = tokenizer.encode(text, disallowed_special=())
    return len(tokens)


def chunk_by_size(text: str, size: int = 50) -> list[Document]:
    """
    Chunk up text recursively.

    :param text: Text to be chunked up
    :return: List of Document items (i.e. chunks).|
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=size,
        chunk_overlap=20,
        length_function=tiktoken_len,
        add_start_index=True,
    )
    return text_splitter.create_documents([text])


# Function will take a string and return an embedding
def vectorizer(text: str):
    return embed.embed_documents([text])[0]
