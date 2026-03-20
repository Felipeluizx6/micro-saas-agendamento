from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import ServicoORM
from app.schemas import ServicoCreate, ServicoResponse

router = APIRouter()


@router.get("/servicos", response_model=list[ServicoResponse])
def listar_servicos():
    db: Session = SessionLocal()
    try:
        servicos = db.query(ServicoORM).all()
        return servicos
    finally:
        db.close()


@router.post("/servicos", response_model=ServicoResponse)
def criar_servico(servico: ServicoCreate):
    db: Session = SessionLocal()
    try:
        novo_servico = ServicoORM(
            nome=servico.nome,
            preco=servico.preco,
            duracao_minutos=servico.duracao_minutos
        )

        db.add(novo_servico)
        db.commit()
        db.refresh(novo_servico)

        return novo_servico
    finally:
        db.close()