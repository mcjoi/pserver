from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API server is running!"}

class Input(BaseModel):
    x: int
    y: int

@app.post("/add")
def add(data: Input):
    return {"result": data.x + data.y}

@app.post("/multi")
def multi(data: Input):
    return {"result": data.x * data.y}



@app.get("/hello")
def hello():
    return {"message": "Hello, this is a new function!"}
