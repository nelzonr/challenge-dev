from sqlalchemy import Column, Boolean, Integer, Float, Date, Time, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Lojas(Base):
    __tablename__ = "lojas"

    id = Column(Integer, primary_key=True, index=True)
    nome_loja = Column(String, unique=True, index=True)

    operacoes = relationship("Operacoes", back_populates="loja")


class Operacoes(Base):
    __tablename__ = "operacoes"

    id = Column(Integer, primary_key=True, index=True)
    tipo_id = Column(Integer, ForeignKey("tipos.id"), nullable=False)
    data = Column(Date)
    valor = Column(Integer)
    cpf = Column(Boolean, default=False)
    cartao = Column(Integer)
    hora = Column(Time)
    dono = Column(String)
    loja_id = Column(Integer, ForeignKey("lojas.id"), nullable=False)

    tipo = relationship("Tipos", back_populates="operacao_tipo")
    loja = relationship("Lojas", back_populates="operacoes")


class Tipos(Base):
    __tablename__ = "tipos"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, unique=True, index=True)
    natureza = Column(String)
    sinal = Column(String)

    operacao_tipo = relationship("Operacoes", back_populates="tipo")
