# Prática 5 — Persistência com PostgreSQL, SQLAlchemy & Migrations

> **Disciplina:** C216 — Sistemas Distribuídos  
> **Módulo:** 3 — Backend & Persistência  
> **Tema:** Persistência PostgreSQL integrada à API com SQLAlchemy e Migrations  
> **Foco:** transformar a API da Prática 4 em uma aplicação que persiste dados de forma organizada, versionada e reproduzível.

---

## 1. De uma API funcional para uma API persistente

Na Prática 4, organizamos a aplicação em uma estrutura de camadas e criamos endpoints com FastAPI.

Até aqui, os dados podem estar apenas em memória:

```text
Cliente
   ↓
HTTP Request
   ↓
FastAPI → Service → dados em memória
                    ↑
             perde ao reiniciar
```

Agora queremos:

```text
Cliente
   ↓
HTTP Request
   ↓
FastAPI
   ↓
Service
   ↓
Repository
   ↓
SQLAlchemy
   ↓
PostgreSQL
```

A partir desta prática, o sistema passa a ter **persistência real**.

---

## 2. Objetivos

Ao final da prática, o aluno deve ser capaz de:

- entender o papel de um banco relacional em uma aplicação web;
- conectar uma aplicação FastAPI ao PostgreSQL;
- utilizar SQLAlchemy como ORM;
- diferenciar **modelo ORM** de **schema Pydantic**;
- organizar a camada de persistência;
- criar operações básicas de CRUD utilizando o banco;
- utilizar migrations para versionar a estrutura do banco;
- executar a aplicação com PostgreSQL via Docker Compose;
- manter configuração de banco através de variáveis de ambiente.

> **Não é objetivo desta prática:** aprofundar SQL avançado, otimização de consultas ou modelagem complexa. O foco é integrar corretamente a persistência ao projeto existente.

---

# 3. PostgreSQL no nosso ambiente

Na Prática 2, já criamos um ambiente distribuído local com Docker Compose.

Agora vamos utilizar efetivamente o serviço:

```text
compose.yml

┌──────────────────────┐
│        API           │
│      FastAPI         │
│                      │
│   :8000              │
└──────────┬───────────┘
           │
           │ DATABASE_URL
           │
           ▼
┌──────────────────────┐
│      PostgreSQL      │
│                      │
│       :5432          │
└──────────────────────┘
```

Dentro da rede do Compose, a API **não** deve utilizar:

```text
localhost
```

Para acessar o PostgreSQL, utilizamos o nome do serviço:

```text
db
```

Exemplo:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/app
```

---

# 4. Dependências

Adicionar ao projeto:

```bash
cd backend

poetry add sqlalchemy psycopg[binary] alembic
```

A ideia é manter:

- **SQLAlchemy** → ORM;
- **psycopg** → driver PostgreSQL;
- **Alembic** → migrations.

Depois:

```bash
poetry install
```

E validar:

```bash
make test
make lint
```

---

# 5. ORM: o que é SQLAlchemy?

Um ORM — **Object-Relational Mapping** — permite representar tabelas do banco através de classes Python.

Por exemplo:

```python
class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
```

A ideia é aproximar:

```text
Python                  PostgreSQL

Classe Item       →     tabela items

id                →     id
name              →     name
description       →     description
```

O SQLAlchemy cuida da comunicação entre os objetos Python e o banco.

> ORM não elimina a necessidade de conhecer SQL. Ele fornece uma camada de abstração para trabalhar com o banco.

---

# 6. Modelo ORM ≠ Schema Pydantic

Esse é um dos pontos mais importantes da prática.

### SQLAlchemy

Representa **como os dados são armazenados**:

```python
class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
```

### Pydantic

Representa **como os dados entram e saem da API**:

```python
class ItemCreate(BaseModel):
    name: str
```

Podemos pensar:

```text
             HTTP
              │
              ▼
       Pydantic Schema
              │
              ▼
           Service
              │
              ▼
       SQLAlchemy Model
              │
              ▼
         PostgreSQL
```

Isso mantém a API desacoplada da estrutura interna do banco.

---

# 7. Organização da persistência

Vamos evoluir a arquitetura definida na Prática 4:

```text
backend/
└── app/
    ├── main.py
    │
    ├── api/
    │   └── routes/
    │
    ├── schemas/
    │
    ├── services/
    │
    ├── repositories/
    │
    ├── models/
    │
    ├── database/
    │   ├── session.py
    │   └── base.py
    │
    └── core/
```

Responsabilidades:

| Camada | Responsabilidade |
|---|---|
| `routes/` | HTTP e endpoints |
| `schemas/` | Entrada e saída da API |
| `services/` | Regras de negócio |
| `repositories/` | Acesso aos dados |
| `models/` | Modelos SQLAlchemy |
| `database/` | conexão e sessão |
| `core/` | configurações e recursos compartilhados |

Fluxo esperado:

```text
Route
  ↓
Service
  ↓
Repository
  ↓
SQLAlchemy
  ↓
PostgreSQL
```

---

# 8. Configurando a conexão

Criar a engine do SQLAlchemy:

```python
from sqlalchemy import create_engine

engine = create_engine(DATABASE_URL)
```

E uma fábrica de sessões:

```python
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
```

Uma dependência do FastAPI pode fornecer a sessão:

```python
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
```

Assim cada requisição pode utilizar uma sessão de banco controlada pela aplicação.

---

# 9. Repository

O repository concentra o acesso aos dados.

Exemplo:

```python
class ItemRepository:

    def __init__(self, db):
        self.db = db

    def create(self, item):
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)

        return item

    def get_all(self):
        return self.db.query(Item).all()
```

A rota não precisa conhecer detalhes do SQLAlchemy:

```text
HTTP
 ↓
Route
 ↓
Service
 ↓
Repository
 ↓
Database
```

Isso também facilita testes e futuras mudanças na implementação da persistência.

---

# 10. CRUD básico

A prática deve transformar pelo menos um recurso existente da Prática 4 em persistente.

Exemplo:

### Criar

```http
POST /items
```

```json
{
  "name": "Notebook"
}
```

### Listar

```http
GET /items
```

### Buscar

```http
GET /items/{id}
```

### Atualizar

```http
PUT /items/{id}
```

### Remover

```http
DELETE /items/{id}
```

O importante não é criar muitos endpoints.

O importante é demonstrar o ciclo completo:

```text
Request
  ↓
FastAPI
  ↓
Service
  ↓
Repository
  ↓
PostgreSQL
  ↓
Response
```

---

# 11. Migrations com Alembic

Um problema aparece quando alteramos o modelo:

```python
class Item(Base):
    ...
    description: Mapped[str | None]
```

Como atualizar o banco?

Não devemos depender de:

```text
"apagar o banco e criar novamente"
```

Em projetos reais, o banco possui dados importantes.

É aí que entram as **migrations**.

Uma migration descreve uma alteração versionada no banco:

```text
Banco v1
   ↓
migration
   ↓
Banco v2
```

---

## 12. Inicializando o Alembic

A partir de `backend/`:

```bash
poetry run alembic init alembic
```

Estrutura esperada:

```text
backend/
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
└── alembic.ini
```

O Alembic precisa conhecer:

1. a URL do banco;
2. os modelos SQLAlchemy.

A configuração deve ser integrada ao projeto em vez de duplicar credenciais diretamente no código.

---

# 13. Criando uma migration

Depois de criar ou alterar um modelo:

```bash
poetry run alembic revision --autogenerate -m "create items"
```

Isso gera uma migration.

Antes de executar, **sempre revise o arquivo gerado**.

Depois:

```bash
poetry run alembic upgrade head
```

Para conferir o estado:

```bash
poetry run alembic current
```

Histórico:

```bash
poetry run alembic history
```

Fluxo:

```text
Alterar Model
     ↓
Gerar Migration
     ↓
Revisar Migration
     ↓
Upgrade
     ↓
PostgreSQL atualizado
```

---

# 14. Docker Compose

O banco já faz parte do ambiente da disciplina.

Subir os serviços:

```bash
make up-build
```

Verificar:

```bash
docker compose ps
```

Logs:

```bash
make logs-api
```

A aplicação deve utilizar:

```text
postgresql+psycopg://...@db:5432/...
```

e não:

```text
postgresql+psycopg://...@localhost:5432/...
```

> `localhost` dentro do container da API aponta para o próprio container da API.

---

# 15. Validando a persistência

Não basta a API responder `200 OK`.

Precisamos verificar se os dados realmente estão sendo persistidos.

### Teste manual

1. Subir API + banco.
2. Criar um registro.
3. Listar os registros.
4. Reiniciar a API.
5. Listar novamente.
6. Confirmar que o registro continua existindo.

Também podemos verificar o banco diretamente:

```bash
docker compose exec db psql -U postgres -d app
```

Exemplo:

```sql
SELECT * FROM items;
```

A ideia é perceber a diferença:

```text
Antes:

POST → memória → reinicia → dados desaparecem

Agora:

POST → PostgreSQL → reinicia → dados continuam
```

---

# 16. Testes

A Prática 3 já criou a infraestrutura de testes.

Agora devemos começar a testar a persistência.

Um teste de integração pode:

```text
criar registro
     ↓
consultar registro
     ↓
verificar resposta
```

Exemplo conceitual:

```python
response = client.post(
    "/items",
    json={"name": "Notebook"},
)

assert response.status_code == 201
```

E depois:

```python
response = client.get("/items")

assert response.status_code == 200
assert len(response.json()) > 0
```

> Nesta prática, o foco é introduzir testes envolvendo persistência. Estratégias mais completas de banco de teste podem ser aprofundadas posteriormente.

---

# 17. Automação com Makefile

Como já utilizamos o `Makefile` como ponto de entrada do projeto, podemos adicionar:

```makefile
db-upgrade:
	cd backend && poetry run alembic upgrade head

db-migration:
	cd backend && poetry run alembic revision --autogenerate -m "$(msg)"

db-current:
	cd backend && poetry run alembic current
```

Uso:

```bash
make db-upgrade
```

ou:

```bash
make db-migration msg="create items"
```

A ideia é evitar que cada desenvolvedor precise decorar comandos internos da ferramenta.

---

# 18. Prática

## Tarefa principal

Evoluir o recurso criado na Prática 4 para utilizar PostgreSQL.

### Requisitos

- [ ] PostgreSQL funcionando pelo Docker Compose;
- [ ] conexão configurada por variável de ambiente;
- [ ] SQLAlchemy integrado ao projeto;
- [ ] pelo menos um modelo ORM;
- [ ] schemas Pydantic separados dos modelos ORM;
- [ ] repository para acesso aos dados;
- [ ] service utilizando o repository;
- [ ] CRUD básico persistido no PostgreSQL;
- [ ] Alembic configurado;
- [ ] pelo menos uma migration criada;
- [ ] aplicação funcionando após reiniciar;
- [ ] testes básicos de integração;
- [ ] `make test` funcionando;
- [ ] `make lint` funcionando.

---

# 19. Resultado esperado

Ao final da prática, o projeto deve ter evoluído de:

```text
FastAPI
  ↓
dados em memória
```

para:

```text
                 ┌──────────────┐
                 │   FastAPI    │
                 └──────┬───────┘
                        ↓
                 ┌──────────────┐
                 │   Services   │
                 └──────┬───────┘
                        ↓
                 ┌──────────────┐
                 │ Repositories │
                 └──────┬───────┘
                        ↓
                 ┌──────────────┐
                 │  SQLAlchemy  │
                 └──────┬───────┘
                        ↓
                 ┌──────────────┐
                 │  PostgreSQL  │
                 └──────────────┘

                  ↑
             Alembic
        versiona o banco
```

O objetivo é que o aluno compreenda que **persistência não é apenas "conectar um banco"**.

Ela envolve:

- modelagem;
- conexão;
- sessões;
- ORM;
- separação de responsabilidades;
- migrations;
- testes;
- configuração;
- execução em ambiente distribuído.

---

# 20. Checklist final

Antes de abrir o PR:

```bash
make format
make lint
make test
make up-build
```

Depois validar:

```text
[ ] API inicia
[ ] PostgreSQL inicia
[ ] migrations executam
[ ] CRUD funciona
[ ] dados permanecem após reiniciar a API
[ ] testes passam
[ ] CI passa
```

### Entrega

A entrega deve conter:

```text
backend/
├── app/
│   ├── api/
│   ├── schemas/
│   ├── services/
│   ├── repositories/
│   ├── models/
│   └── database/
│
├── alembic/
│   └── versions/
│
├── tests/
├── alembic.ini
└── pyproject.toml
```

E uma migration que permita reproduzir a estrutura do banco a partir de um banco vazio.

---

## Conexão com a próxima prática

Até aqui:

```text
Prática 1 → Git + Poetry + Makefile
Prática 2 → Docker + Compose
Prática 3 → Testes + CI
Prática 4 → Arquitetura + FastAPI
Prática 5 → PostgreSQL + SQLAlchemy + Migrations
```

Na próxima etapa, o backend já terá uma base persistente sobre a qual o **frontend em JavaScript** poderá começar a consumir a API.
