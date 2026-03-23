from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_empresa_id, get_db
from app.database.models import AgendamentoORM, ClienteORM, ProfissionalORM
from app.schemas import AgendamentoCreate, AgendamentoResponse

router = APIRouter()


@router.get("/agendamentos", response_model=list[AgendamentoResponse])
def listar_agendamentos(
    empresa_id: int = Depends(get_current_empresa_id),
    db: Session = Depends(get_db)
):
    agendamentos = db.query(AgendamentoORM).filter(
        AgendamentoORM.empresa_id == empresa_id
    ).order_by(
        AgendamentoORM.data,
        AgendamentoORM.hora
    ).all()

    return agendamentos


@router.post("/agendamentos", response_model=AgendamentoResponse)
def criar_agendamento(
    agendamento: AgendamentoCreate,
    empresa_id: int = Depends(get_current_empresa_id),
    db: Session = Depends(get_db)
):
    cliente = db.query(ClienteORM).filter(
        ClienteORM.id == agendamento.cliente_id,
        ClienteORM.empresa_id == empresa_id
    ).first()

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado para esta empresa."
        )

    profissional = db.query(ProfissionalORM).filter(
        ProfissionalORM.id == agendamento.profissional_id,
        ProfissionalORM.empresa_id == empresa_id
    ).first()

    if not profissional:
        raise HTTPException(
            status_code=404,
            detail="Profissional não encontrado para esta empresa."
        )

    conflito = db.query(AgendamentoORM).filter(
        AgendamentoORM.empresa_id == empresa_id,
        AgendamentoORM.profissional_id == agendamento.profissional_id,
        AgendamentoORM.data == agendamento.data,
        AgendamentoORM.hora == agendamento.hora
    ).first()

    if conflito:
        raise HTTPException(
            status_code=400,
            detail="Este profissional já possui um agendamento neste horário."
        )

    novo_agendamento = AgendamentoORM(
        cliente_id=agendamento.cliente_id,
        profissional_id=agendamento.profissional_id,
        empresa_id=empresa_id,
        data=agendamento.data,
        hora=agendamento.hora,
        servico=agendamento.servico
    )

    db.add(novo_agendamento)
    db.commit()
    db.refresh(novo_agendamento)

    return novo_agendamento


@router.get("/agenda", response_model=list[AgendamentoResponse])
def agenda_dia(
    profissional_id: Optional[int] = None,
    data: Optional[date] = None,
    empresa_id: int = Depends(get_current_empresa_id),
    db: Session = Depends(get_db)
):
    query = db.query(AgendamentoORM).filter(
        AgendamentoORM.empresa_id == empresa_id
    )

    if profissional_id is not None:
        query = query.filter(
            AgendamentoORM.profissional_id == profissional_id
        )

    if data is not None:
        query = query.filter(
            AgendamentoORM.data == data
        )

    agendamentos = query.order_by(
        AgendamentoORM.data,
        AgendamentoORM.hora
    ).all()

    return agendamentos


@router.put("/agendamentos/{agendamento_id}", response_model=AgendamentoResponse)
def atualizar_agendamento(
    agendamento_id: int,
    dados: AgendamentoCreate,
    empresa_id: int = Depends(get_current_empresa_id),
    db: Session = Depends(get_db)
):
    agendamento = db.query(AgendamentoORM).filter(
        AgendamentoORM.id == agendamento_id,
        AgendamentoORM.empresa_id == empresa_id
    ).first()

    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    cliente = db.query(ClienteORM).filter(
        ClienteORM.id == dados.cliente_id,
        ClienteORM.empresa_id == empresa_id
    ).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado para esta empresa.")

    profissional = db.query(ProfissionalORM).filter(
        ProfissionalORM.id == dados.profissional_id,
        ProfissionalORM.empresa_id == empresa_id
    ).first()

    if not profissional:
        raise HTTPException(status_code=404, detail="Profissional não encontrado para esta empresa.")

    conflito = db.query(AgendamentoORM).filter(
        AgendamentoORM.empresa_id == empresa_id,
        AgendamentoORM.profissional_id == dados.profissional_id,
        AgendamentoORM.data == dados.data,
        AgendamentoORM.hora == dados.hora,
        AgendamentoORM.id != agendamento_id
    ).first()

    if conflito:
        raise HTTPException(
            status_code=400,
            detail="Este profissional já possui um agendamento neste horário."
        )

    agendamento.cliente_id = dados.cliente_id
    agendamento.profissional_id = dados.profissional_id
    agendamento.data = dados.data
    agendamento.hora = dados.hora
    agendamento.servico = dados.servico

    db.commit()
    db.refresh(agendamento)

    return agendamento


@router.delete("/agendamentos/{agendamento_id}")
def deletar_agendamento(
    agendamento_id: int,
    empresa_id: int = Depends(get_current_empresa_id),
    db: Session = Depends(get_db)
):
    agendamento = db.query(AgendamentoORM).filter(
        AgendamentoORM.id == agendamento_id,
        AgendamentoORM.empresa_id == empresa_id
    ).first()

    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    db.delete(agendamento)
    db.commit()

    return {"mensagem": "Agendamento deletado com sucesso"}