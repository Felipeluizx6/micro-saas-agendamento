from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#from app.database.init_db import init_db

from app.routes.auth import router as auth_router
from app.routes.profissionais import router as profissionais_router
from app.routes.clientes import router as clientes_router
from app.routes.servicos import router as servicos_router
from app.routes.agendamentos import router as agendamentos_router

#init_db()

app = FastAPI(title="Micro SaaS Agendamento")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(clientes_router)
app.include_router(profissionais_router)
app.include_router(servicos_router)
app.include_router(agendamentos_router)


@app.get("/")
def home():
    return {
        "status": "ok",
        "mensagem": "API Micro SaaS rodando",
        "multiempresa": True,
        "auth": True
    }