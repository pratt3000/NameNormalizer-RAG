# How to test API endpoint
Pass you alternative company name to `http://44.203.139.218:8888/pm/{unnormalized_company_name}`

ex - `http://44.203.139.218:8888/pm/deepmind`

It should return something like 
```
{
  "query": "deepmind",
  "output": "{'normalized company name': 'Google', 'eucledian distance': 0.24236941, 'vector_text': 'DeepMind'}"
}
```

### Troubleshooting:
Check if the service is up at `http://44.203.139.218:8888/`. It should return hello world followed by a random integer everytime.



# How to run Locally
## Pre-setup
1. create a .env file and copy the following enviroment variables into it.
    ```
    OPENAI_API_KEY = "xxx"
    QDRANT_API_KEY = "xxx"
    QDRANT_CLOUD = "xxx.cloud.qdrant.io"
    ```

2. create a folder `postgresdata` in the main working directory

## How to (actually) run it locally:

1. To spin up all things simply type `make deploy` in your terminal. (Docker needed)

    (Optional - to see logs run `make logs`) 

2. Visit `http://0.0.0.0:8888` and test endpoints.

    1. The api endpoint for normalizing merchant names is `http://0.0.0.0:8888/pm/{alternative_merchant_name}`. This will return the closest normalized company name, along with other details.

4. To stop `make all_down`

## Testing
1. To test run `tests.py`. If no exceptions arise, everything is working.

    p.s. Didnt get time to write better tests. TODO.