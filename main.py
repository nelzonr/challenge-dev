from fastapi import FastAPI, UploadFile
from typing import List

app = FastAPI()

@app.get("/")
def hello_world():
    return {"message": "Hello World"}

@app.post("/upload")
async def upload_files(files: List[UploadFile]):
    output = []
    for file in files:
        output.append({"filename": file.filename, "contents": await file.read()})

    return {"output": output}
