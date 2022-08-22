from fastapi import FastAPI, Depends, UploadFile, HTTPException
from typing import List
from pydantic import BaseModel, constr
from sqlalchemy.orm import Session
import re
from database import engine, SessionLocal
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


class CNAE(BaseModel):
    tipo: constr(min_length=1, max_length=1) = '5'
    data: constr(min_length=8, max_length=8) = '20190301'
    valor: constr(min_length=11, max_length=11) = '00000132005'
    cpf: constr(min_length=11, max_length=11) = '56418150633'
    cartao: constr(min_length=11, max_length=11) = '123****7687'
    hora: constr(min_length=6, max_length=6) = '145607'
    dono: constr(min_length=14, max_length=14) = 'MARIA JOSEFINA'
    loja: constr(min_length=1, max_length=18) = 'LOJA DO Ó - MATRIZ'


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post("/cnae")
async def create_cnae(cnae: CNAE, db: Session = Depends(get_db)):
    operacao_model = models.CNAE()
    operacao_model.tipo = cnae.tipo
    operacao_model.data = cnae.data
    operacao_model.valor = cnae.valor
    operacao_model.cpf = cnae.cpf
    operacao_model.cartao = cnae.cartao
    operacao_model.hora = cnae.hora
    operacao_model.dono = cnae.dono
    operacao_model.loja = cnae.loja
    operacao_model.processed = False

    db.add(operacao_model)
    db.commit()

    return {'status': 201, 'transaction': 'Successful'}

@app.get("/tipos")
async def read_all_tipos(db: Session = Depends(get_db)):
    return db.query(models.Tipos).all()


@app.get("/tipos/{tipo_id}")
async def read_tipo(tipo_id: int, db: Session = Depends(get_db)):
    tipo_model = db.query(models.Tipos)\
        .filter(models.Tipos.id == tipo_id)\
        .first()
    if tipo_model is not None:
        return tipo_model
    raise http_exception()


@app.post("/upload")
async def upload_files(files: List[UploadFile], db: Session = Depends(get_db)):
    all_contents = []
    for file in files:
        contents = await file.read()
        all_contents.append(contents)
        await upload_save(contents, db)

    return {"output": all_contents}


async def upload_save(contents, db: Session = Depends(get_db)):
    registros = line2operation(contents)

    for registro in registros:
        operacao_model = models.Operacoes()
        operacao_model.tipo = registro[0]
        operacao_model.data = registro[1]
        operacao_model.valor = registro[2]
        operacao_model.cpf = registro[3]
        operacao_model.cartao = registro[4]
        operacao_model.hora = registro[5]
        operacao_model.dono = registro[6]
        operacao_model.loja = registro[7]
        db.add(operacao_model)

    db.commit()


@app.get("/operacoes")
async def read_all_operacoes(db: Session = Depends(get_db)):
    return db.query(models.Operacoes).all()



def line2operation(text):
    operation = re.findall(b"(\d{1})(\d{8})(\d{11})(\d{11})(.{11})(\d{6})(.{14})(.{1,})", text)
    return operation


def http_exception(status_code=404, message="Not found"):
    return HTTPException(status_code=status_code, detail=message)
