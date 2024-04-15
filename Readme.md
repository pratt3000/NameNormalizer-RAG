# Setup

1. create a .env file and copy the enviroment variables into it.
    ```
    OPENAI_API_KEY = "xxx"
    QDRANT_API_KEY = "xxx"
    QDRANT_CLOUD = "xxx.cloud.qdrant.io"
    ```

2. create a folder `postgresdata` in the main working directory

# How to run:

1. To initialize a small dummy index with some dummy data run initialize_index() in main.py
2. `make deploy`
3. Optional - to see logs `make logs` 
4. visit `http://0.0.0.0:8888` and the api endpoint for putting in alternative merchant names is http://0.0.0.0:8888/pm/{alternative_merchant_name}. This will return the closest normalized company name.
5. To stop `make all_down`

