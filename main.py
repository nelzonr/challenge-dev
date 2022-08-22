from fastapi import FastAPI, UploadFile
from typing import List

app = FastAPI()

@app.get("/")
def hello_world():
    return {"message": "Hello World"}
