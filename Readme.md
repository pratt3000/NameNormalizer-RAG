# Setup

1. create a .env file and copy the enviroment variables into it.
    ```
    OPENAI_API_KEY = "xxx"
    PINECONE_API_KEY = "xxx"
    ```

2. create a folder `postgresdata` in the main working directory

# How to run:

1. To initialize a small dummy index with some dummy data run initialize_index() in main.py
2. `make deploy`
3. visit `http://0.0.0.0:8888`
4. To stop `make all_down`

### Comprehensive:
1. Just write `make run` in the terminal.
