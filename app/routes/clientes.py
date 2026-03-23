from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_empresa_id, get_db
from app.database.models import ClienteORM
from app.schemas import ClienteCreate, ClienteResponse

router = APIRouter()


@router.get("/clientes", response_model=list[ClienteResponse])
def listar_clientes(
    empresa_id: int = Depends(get_current_empresa_id),
    db: Session = Depends(get_db)
):
    clientes = db.query(ClienteORM).filter(
        ClienteORM.empresa_id == empresa_id
    ).all()
    return clientes


@router.post("/clientes", response_model=ClienteResponse)
def criar_cliente(
    cliente: ClienteCreate,
    empresa_id: int = Depends(get_current_empresa_id),
    db: Session = Depends(get_db)
):
    novo_cliente = ClienteORM(
        nome=cliente.nome,
        telefone=cliente.telefone,
        empresa_id=empresa_id
    )

    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)

    return novo_cliente