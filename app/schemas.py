from pydantic import BaseModel, ConfigDict, EmailStr


# =========================
# AUTH / EMPRESA / USUÁRIO
# =========================

class RegisterRequest(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    empresa_nome: str
    empresa_email: EmailStr | None = None
    empresa_telefone: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    empresa_id: int

    model_config = ConfigDict(from_attributes=True)


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
# SERVIÇOS
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
    servico: str


class AgendamentoResponse(BaseModel):
    id: int
    cliente_id: int
    profissional_id: int
    data: str
    hora: str
    servico: str

    model_config = ConfigDict(from_attributes=True)