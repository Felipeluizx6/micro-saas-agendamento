from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_empresa_id, get_db
from app.database.models import ServicoORM
from app.schemas import ServicoCreate, ServicoResponse

router = APIRouter()


@router.get("/servicos", response_model=list[ServicoResponse])
def listar_servicos(
    empresa_id: int = Depends(get_current_empresa_id),
    db: Session = Depends(get_db)
):
    servicos = db.query(ServicoORM).filter(
        ServicoORM.empresa_id == empresa_id
    ).all()
    return servicos


@router.post("/servicos", response_model=ServicoResponse)
def criar_servico(
    servico: ServicoCreate,
    empresa_id: int = Depends(get_current_empresa_id),
    db: Session = Depends(get_db)
):
    novo_servico = ServicoORM(
        nome=servico.nome,
        preco=servico.preco,
        duracao_minutos=servico.duracao_minutos,
        empresa_id=empresa_id
    )

    db.add(novo_servico)
    db.commit()
    db.refresh(novo_servico)

    return novo_servico