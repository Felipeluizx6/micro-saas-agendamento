from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import (
    autenticar_usuario,
    criar_access_token,
    gerar_hash_senha,
    get_current_user,
    get_db,
    obter_usuario_por_email,
)
from app.database.models import EmpresaORM, UsuarioORM
from app.schemas import LoginRequest, RegisterRequest, TokenResponse, UsuarioResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UsuarioResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    usuario_existente = obter_usuario_por_email(db, data.email)
    if usuario_existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")

    nova_empresa = EmpresaORM(
        nome=data.empresa_nome,
        email=data.empresa_email,
        telefone=data.empresa_telefone
    )
    db.add(nova_empresa)
    db.commit()
    db.refresh(nova_empresa)

    novo_usuario = UsuarioORM(
        nome=data.nome,
        email=data.email,
        senha_hash=gerar_hash_senha(data.senha),
        empresa_id=nova_empresa.id
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    usuario = autenticar_usuario(db, data.email, data.senha)

    if not usuario:
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos.")

    token = criar_access_token(
        data={
            "sub": usuario.id,
            "empresa_id": usuario.empresa_id,
            "email": usuario.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UsuarioResponse)
def me(usuario: UsuarioORM = Depends(get_current_user)):
    return usuario