from pydantic import BaseModel, ConfigDict


# =========================
# PROFISSIONAIS
# =========================

class ProfissionalCreate(BaseModel):
    nome: str
    telefone: str
    servico: str


class ProfissionalResponse(BaseModel):
    id: int
    nome: str
    telefone: str
    servico: str

    model_config = ConfigDict(from_attributes=True)


# =========================
# CLIENTES
# =========================

class ClienteCreate(BaseModel):
    nome: str
    telefone: str


class ClienteResponse(BaseModel):
    id: int
    nome: str
    telefone: str

    model_config = ConfigDict(from_attributes=True)


# =========================
# SERVIÇOS (NOVO)
# =========================

class ServicoCreate(BaseModel):
    nome: str
    preco: int
    duracao_minutos: int


class ServicoResponse(BaseModel):
    id: int
    nome: str
    preco: int
    duracao_minutos: int

    model_config = ConfigDict(from_attributes=True)


# =========================
# AGENDAMENTOS
# =========================

class AgendamentoCreate(BaseModel):
    cliente_id: int
    profissional_id: int
    data: str
    hora: str
    servico: str  # ainda evoluir para servico_id


class AgendamentoResponse(BaseModel):
    id: int
    cliente_id: int
    profissional_id: int
    data: str
    hora: str
    servico: str

    model_config = ConfigDict(from_attributes=True)