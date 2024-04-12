from fastapi import FastAPI
import random
import uvicorn

from src.main import get_topk_matches

app = FastAPI()

@app.get("/pm/{query}")
async def get_merchant(query: str = None):
    res = get_topk_matches(query, top_k=1)
    
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