from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import ProfissionalORM
from app.schemas import ProfissionalCreate, ProfissionalResponse

router = APIRouter()


@router.get("/profissionais", response_model=list[ProfissionalResponse])
def listar_profissionais():
    db: Session = SessionLocal()
    try:
        profissionais = db.query(ProfissionalORM).all()
        return profissionais
    finally:
        db.close()


@router.post("/profissionais", response_model=ProfissionalResponse)
def criar_profissional(profissional: ProfissionalCreate):
    db: Session = SessionLocal()
    try:
        novo_profissional = ProfissionalORM(
            nome=profissional.nome,
            telefone=profissional.telefone,
            servico=profissional.servico
        )
        db.add(novo_profissional)
        db.commit()
        db.refresh(novo_profissional)
        return novo_profissional
    finally:
        db.close()