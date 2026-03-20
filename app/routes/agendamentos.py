from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import AgendamentoORM
from app.schemas import AgendamentoCreate, AgendamentoResponse

router = APIRouter()


@router.get("/agendamentos", response_model=list[AgendamentoResponse])
def listar_agendamentos():
    db: Session = SessionLocal()
    try:
        agendamentos = db.query(AgendamentoORM).all()
        return agendamentos
    finally:
        db.close()


@router.post("/agendamentos", response_model=AgendamentoResponse)
def criar_agendamento(agendamento: AgendamentoCreate):
    db: Session = SessionLocal()
    try:
        conflito = db.query(AgendamentoORM).filter(
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
            data=agendamento.data,
            hora=agendamento.hora,
            servico=agendamento.servico
        )

        db.add(novo_agendamento)
        db.commit()
        db.refresh(novo_agendamento)

        return novo_agendamento

    finally:
        db.close()