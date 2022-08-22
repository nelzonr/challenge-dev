from fastapi import FastAPI, Depends, UploadFile, HTTPException
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


@app.get("/tipos")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Tipos).all()


@app.get("/tipos/{tipo_id}")
async def read_tipo(tipo_id: int, db: Session = Depends(get_db)):
    tipo_model = db.query(models.Tipos)\
        .filter(models.Tipos.id == tipo_id)\
        .first()
    if tipo_model is not None:
        return tipo_model
    raise http_exception()


def http_exception(status_code=404, message="Not found"):
    return HTTPException(status_code=status_code, detail=message)
