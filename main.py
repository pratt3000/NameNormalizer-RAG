from fastapi import FastAPI
import random
import uvicorn

from src.main import process_query

app = FastAPI()

@app.get("/pm/{query}")
async def get_merchant(query: str = None):
    res = process_query(query, top_k=1, threshold=0.5)
    
    output = {
        "query": query, 
        "output": str(res)
    }
    return output

@app.get("/")
async def root(query: str = None):
    return {"message": f"Hello World {random.randint(1, 100)}"}

if __name__ == "__main__":
    uvicorn.run(app, port=8888)