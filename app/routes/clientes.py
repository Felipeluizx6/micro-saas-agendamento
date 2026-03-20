from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import ClienteORM
from app.schemas import ClienteCreate, ClienteResponse

router = APIRouter()


@router.get("/clientes", response_model=list[ClienteResponse])
def listar_clientes():
    db: Session = SessionLocal()
    try:
        clientes = db.query(ClienteORM).all()
        return clientes
    finally:
        db.close()


@router.post("/clientes", response_model=ClienteResponse)
def criar_cliente(cliente: ClienteCreate):
    db: Session = SessionLocal()
    try:
        novo_cliente = ClienteORM(
            nome=cliente.nome,
            telefone=cliente.telefone
        )
        db.add(novo_cliente)
        db.commit()
        db.refresh(novo_cliente)
        return novo_cliente
    finally:
        db.close()