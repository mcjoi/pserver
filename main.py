from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class InputData(BaseModel):
    x: int
    y: int

@app.post("/add")
def add_numbers(data: InputData):
    return {"result": data.x + data.y}