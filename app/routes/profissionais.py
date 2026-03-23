from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_empresa_id, get_db
from app.database.models import ProfissionalORM
from app.schemas import ProfissionalCreate, ProfissionalResponse

router = APIRouter()


@router.get("/profissionais", response_model=list[ProfissionalResponse])
def listar_profissionais(
    empresa_id: int = Depends(get_current_empresa_id),
    db: Session = Depends(get_db)
):
    profissionais = db.query(ProfissionalORM).filter(
        ProfissionalORM.empresa_id == empresa_id
    ).all()
    return profissionais


@router.post("/profissionais", response_model=ProfissionalResponse)
def criar_profissional(
    profissional: ProfissionalCreate,
    empresa_id: int = Depends(get_current_empresa_id),
    db: Session = Depends(get_db)
):
    novo_profissional = ProfissionalORM(
        nome=profissional.nome,
        telefone=profissional.telefone,
        servico=profissional.servico,
        empresa_id=empresa_id
    )

    db.add(novo_profissional)
    db.commit()
    db.refresh(novo_profissional)

    return novo_profissional