Micro SaaS - Sistema de Agendamento Inteligente

Sistema backend para gerenciamento de agendamentos, clientes, profissionais e serviços, com foco em negócios como salão de beleza, estética e clínicas.

🚀 Visão Geral

API REST desenvolvida para:

- Gestão de agendamentos
- Controle de clientes
- Gerenciamento de profissionais
- Organização de serviços
- Estrutura pronta para SaaS escalável

🧠 Arquitetura do Sistema

📦 app
 ┣ 📂 database
 ┃ ┣ 📜 connection.py
 ┃ ┣ 📜 init_db.py
 ┃ ┗ 📜 models.py
 ┣ 📂 routes
 ┃ ┣ 📜 clientes.py
 ┃ ┣ 📜 profissionais.py
 ┃ ┣ 📜 agendamentos.py
 ┃ ┗ 📜 servicos.py
 ┣ 📜 schemas.py
 ┗ 📜 main.py


⚙️ Tecnologias Utilizadas

Backend

- Python 3.14
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn

Banco de Dados

- PostgreSQL

Versionamento

- Git & GitHub

Futuro (Stack planejada)

- HTML
- CSS
- JavaScript
- Java (possível uso em microserviços)


🧪 Funcionalidades Implementadas

✔️ Profissionais

- Criar profissional
- Listar profissionais

✔️ Clientes

- Criar cliente
- Listar clientes

✔️ Agendamentos

- Criar agendamento
- Listar agendamentos
- Validação de conflito de horário

✔️ Serviços

- Criar serviço
- Listar serviços


🔐 Boas Práticas Aplicadas

- Arquitetura modular (routes, models, schemas)
- Uso de ORM (SQLAlchemy)
- Validação de dados com Pydantic
- Separação de responsabilidades
- Uso de variáveis de ambiente (.env)
- Gitignore configurado corretamente
- Estrutura preparada para escalabilidade


📡 Execução do Projeto

# Ativar ambiente virtual
venv\Scripts\activate

# Rodar servidor
python -m uvicorn app.main:app --reload

Acesse a documentação interativa:

http://localhost:8000/docs


📊 Próximas Implementações

- 📈 Dashboard (relatórios e métricas)
- 💰 Controle financeiro (entrada/saída)
- 🔐 Autenticação e autorização (JWT)
- 🏢 Multiempresa (SaaS real)
- 🌐 Frontend (HTML, CSS, JavaScript)
- ☕ Possível integração com Java (microserviços)

🎯 Objetivo do Projeto

Desenvolver um sistema SaaS leve, escalável e orientado a dados para pequenos negócios, permitindo:

- Melhor organização operacional
- Automação de processos
- Tomada de decisão baseada em dados

🧠 Diferencial Técnico

- Backend desacoplado
- Estrutura pronta para crescimento
- Foco em performance e simplicidade
- Preparado para integração com dashboards e analytics


📌 Status

🚧 Em desenvolvimento (versão funcional inicial)