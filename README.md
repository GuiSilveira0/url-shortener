<div align="center">

# 🔗 URL Shortener

**Encurtador de URLs moderno com analytics em tempo real**

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?logo=postgresql&logoColor=white)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis&logoColor=white)](https://redis.io)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://docker.com)

</div>

---

## 📋 Sobre o Projeto

API RESTful para encurtamento de URLs construída com **FastAPI**, seguindo princípios de **Clean Architecture**. Além de encurtar links, o serviço oferece **analytics detalhado** com rastreamento de cliques, geolocalização, dispositivos e navegadores — tudo com cache em Redis para performance em tempo real.

### ✨ Funcionalidades

- 🔗 **Encurtamento de URLs** — Gera códigos curtos únicos automaticamente
- 📊 **Analytics completo** — Total de cliques, visitantes únicos, distribuição por país, dispositivo e navegador
- ⚡ **Estatísticas em tempo real** — Cache Redis para consultas instantâneas
- 📈 **Analytics por período** — Cliques por dia com filtro de datas
- 🌍 **Geolocalização** — Identifica país e cidade do visitante via IP
- 🔄 **Redirecionamento automático** — Acesse `/{short_code}` e seja redirecionado
- 🐳 **100% containerizado** — Suba tudo com um único comando

---

## 🏗️ Arquitetura

O projeto segue **Clean Architecture** com separação clara de responsabilidades:

```
app/
├── controller/      → Rotas HTTP (FastAPI Routers)
├── entities/        → Modelos de domínio (Pydantic)
├── gateway/         → Interfaces/contratos dos repositórios
└── usecase/         → Regras de negócio

infrastructure/
├── db/sql/          → PostgreSQL (persistência)
├── db/redis/        → Redis (cache + analytics real-time)
├── services/        → Serviços externos (GeoIP, User-Agent)
└── config.py        → Configuração centralizada
```

**Fluxo de dependências:** Controller → Use Case → Gateway ← Repository (Infrastructure)

---

## 🚀 Como Executar

### Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/install/)

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/url-shortener.git
cd url-shortener
```

### 2. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=sua_senha
POSTGRES_DB=url_shortener
DATABASE_URL=postgresql://postgres:sua_senha@db:5432/url_shortener

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_BASE=0
REDIS_URL=redis://redis:6379/0
REDIS_USERNAME=
REDIS_PASSWORD=

API_BASE_URL=http://localhost:8000
```

### 3. Suba os containers

```bash
docker-compose up -d
```

Pronto! A aplicação estará disponível em `http://localhost:8000`.

---

## 📡 Endpoints da API

### URL Shortener

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/api/v1/shorten` | Encurta uma URL |
| `GET` | `/{short_code}` | Redireciona para a URL original |

### Analytics

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/v1/stats/{short_code}` | Estatísticas gerais do link |
| `GET` | `/api/v1/analytics/{short_code}` | Analytics detalhado com filtro por período |
| `GET` | `/api/v1/analytics/{short_code}/realtime` | Estatísticas em tempo real (Redis) |

### Exemplos

**Encurtar uma URL:**
```bash
curl -X POST http://localhost:8000/api/v1/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://exemplo.com/uma-url-muito-longa"}'
```

**Resposta:**
```json
{
  "original_url": "https://exemplo.com/uma-url-muito-longa",
  "short_code": "aB3xY9",
  "short_url": "http://localhost:8000/aB3xY9"
}
```

**Consultar estatísticas:**
```bash
curl http://localhost:8000/api/v1/stats/aB3xY9
```

---

## 🛠️ Tech Stack

| Tecnologia | Uso |
|------------|-----|
| **FastAPI** | Framework web / API REST |
| **PostgreSQL 15** | Banco de dados principal |
| **Redis 7** | Cache e analytics em tempo real |
| **SQLAlchemy** | ORM para acesso ao banco |
| **Alembic** | Migrações de banco de dados |
| **Pydantic** | Validação de dados e configuração |
| **Docker Compose** | Orquestração de containers |
| **Adminer** | Interface web para gerenciar o banco |

---

## 🔧 Desenvolvimento Local (sem Docker)

```bash
# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

> ⚠️ Certifique-se de ter PostgreSQL e Redis rodando localmente e as variáveis de ambiente configuradas.

---

## 📚 Links Úteis

| Recurso | URL |
|---------|-----|
| API (Swagger UI) | http://localhost:8000/docs |
| API (ReDoc) | http://localhost:8000/redoc |
| Adminer (DB Admin) | http://localhost:8080 |
| Health Check | http://localhost:8000 |

---