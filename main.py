from fastapi import FastAPI
import random
import uvicorn

from src.main import get_main_entity

app = FastAPI()

@app.get("/pm/{query}")
async def get_merchant(query: str = None):
    merchant_name = get_main_entity(query)
    return {"query": query, "result": merchant_name}

@app.get("/")
async def root(query: str = None):
    return {"message": f"Hello World {random.randint(1, 100)}"}

if __name__ == '__main__':
    uvicorn.run(app, port=8888)