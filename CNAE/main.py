from fastapi import FastAPI, UploadFile
from typing import List
from database import engine
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def create_database():
    return {"Database": "Created"}
