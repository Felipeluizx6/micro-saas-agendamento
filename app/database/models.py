from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base


class ProfissionalORM(Base):
    __tablename__ = "profissionais"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    servico = Column(String, nullable=False)

    agendamentos = relationship("AgendamentoORM", back_populates="profissional")


class ClienteORM(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    telefone = Column(String, nullable=False)

    agendamentos = relationship("AgendamentoORM", back_populates="cliente")


class AgendamentoORM(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)

    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    profissional_id = Column(Integer, ForeignKey("profissionais.id"))

    data = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    servico = Column(String, nullable=False)

    cliente = relationship("ClienteORM", back_populates="agendamentos")
    profissional = relationship("ProfissionalORM", back_populates="agendamentos")


class ServicoORM(Base):
    __tablename__ = "servicos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    preco = Column(Integer, nullable=False)
    duracao_minutos = Column(Integer, nullable=False)