from fastapi import FastAPI
from app.database.init_db import init_db
from app.routes.profissionais import router as profissionais_router
from app.routes.clientes import router as clientes_router
from app.routes.agendamentos import router as agendamentos_router
from app.routes.servicos import router as servicos_router

init_db()

app = FastAPI()

app.include_router(profissionais_router)
app.include_router(clientes_router)
app.include_router(agendamentos_router)
app.include_router(servicos_router)


@app.get("/")
def home():
    return {"mensagem": "Micro SaaS rodando com PostgreSQL"}