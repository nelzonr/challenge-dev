from fastapi import FastAPI, Depends, UploadFile
from typing import List
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()
