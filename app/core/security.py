from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import UsuarioORM

SECRET_KEY = "troque_essa_chave_em_producao_123456789"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def gerar_hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)


def verificar_senha(senha: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha, senha_hash)


def criar_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def obter_usuario_por_email(db: Session, email: str) -> UsuarioORM | None:
    return db.query(UsuarioORM).filter(UsuarioORM.email == email).first()


def autenticar_usuario(db: Session, email: str, senha: str) -> UsuarioORM | None:
    usuario = obter_usuario_por_email(db, email)
    if not usuario:
        return None

    if not verificar_senha(senha, usuario.senha_hash):
        return None

    return usuario


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UsuarioORM:
    credenciais_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int | None = payload.get("sub")
        if user_id is None:
            raise credenciais_exception
    except JWTError:
        raise credenciais_exception

    usuario = db.query(UsuarioORM).filter(UsuarioORM.id == user_id).first()
    if usuario is None:
        raise credenciais_exception

    return usuario


def get_current_empresa_id(
    usuario: UsuarioORM = Depends(get_current_user)
) -> int:
    return usuario.empresa_id