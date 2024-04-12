from fastapi import FastAPI
import random
import uvicorn

app = FastAPI()

@app.get("/patternMatcher/{query}")
async def root(query: str = None):
    return {"message": f"Hello World {random.randint(1, 100)}", "query": query}

@app.get("/")
async def root(query: str = None):
    return {"message": f"Hello World"}

if __name__ == '__main__':
    uvicorn.run(app, port=8888)