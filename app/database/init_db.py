from app.database.connection import engine, Base, SessionLocal
from app.database import models
from app.database.models import EmpresaORM


def criar_empresa_padrao():
    db = SessionLocal()
    try:
        empresa = db.query(EmpresaORM).first()

        if not empresa:
            nova_empresa = EmpresaORM(
                nome="Empresa Padrão",
                email="contato@empresa.com",
                telefone="000000000"
            )
            db.add(nova_empresa)
            db.commit()
    finally:
        db.close()


def init_db():
    # Primeiro cria as tabelas
    Base.metadata.create_all(bind=engine)

    # Só depois insere a empresa padrão
    criar_empresa_padrao()