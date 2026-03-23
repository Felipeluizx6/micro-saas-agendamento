from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base


class EmpresaORM(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=True)
    telefone = Column(String, nullable=True)

    clientes = relationship("ClienteORM", back_populates="empresa")
    profissionais = relationship("ProfissionalORM", back_populates="empresa")
    servicos = relationship("ServicoORM", back_populates="empresa")
    agendamentos = relationship("AgendamentoORM", back_populates="empresa")
    usuarios = relationship("UsuarioORM", back_populates="empresa")


class UsuarioORM(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)

    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)

    empresa = relationship("EmpresaORM", back_populates="usuarios")


class ProfissionalORM(Base):
    __tablename__ = "profissionais"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    servico = Column(String, nullable=False)

    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)

    empresa = relationship("EmpresaORM", back_populates="profissionais")
    agendamentos = relationship("AgendamentoORM", back_populates="profissional")


class ClienteORM(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    telefone = Column(String, nullable=False)

    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)

    empresa = relationship("EmpresaORM", back_populates="clientes")
    agendamentos = relationship("AgendamentoORM", back_populates="cliente")


class ServicoORM(Base):
    __tablename__ = "servicos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    preco = Column(Integer, nullable=False)
    duracao_minutos = Column(Integer, nullable=False)

    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)

    empresa = relationship("EmpresaORM", back_populates="servicos")


class AgendamentoORM(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)

    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    profissional_id = Column(Integer, ForeignKey("profissionais.id"), nullable=False)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)

    data = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    servico = Column(String, nullable=False)

    cliente = relationship("ClienteORM", back_populates="agendamentos")
    profissional = relationship("ProfissionalORM", back_populates="agendamentos")
    empresa = relationship("EmpresaORM", back_populates="agendamentos")