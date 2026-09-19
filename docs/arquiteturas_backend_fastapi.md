# Prática 4 — Arquiteturas & APIs com FastAPI

> **Disciplina:** C216 — Sistemas Distribuídos  
> **Módulo:** Backend & Persistência  
> **Foco:** Organização estrutural de projetos, arquiteturas de software, APIs e endpoints com FastAPI

---

## 1. Objetivos da aula

Ao final da prática, o aluno deverá ser capaz de:

- entender por que projetos precisam de uma organização arquitetural;
- diferenciar **arquitetura**, **camada**, **componente** e **padrão**;
- reconhecer arquiteturas comuns em aplicações web;
- entender o papel de uma API e de seus endpoints;
- criar endpoints básicos utilizando FastAPI;
- organizar uma API em uma estrutura de projeto mais sustentável.

> **Ideia central:** arquitetura não é apenas "onde colocar arquivos". Ela define como as responsabilidades do sistema são organizadas e como seus componentes se relacionam.

---

# 2. O problema: quando o projeto cresce

Um projeto pequeno pode começar assim:

```text
backend/
├── main.py
└── pyproject.toml
```

E funcionar perfeitamente.

Mas, conforme aparecem:

- vários endpoints;
- regras de negócio;
- acesso ao banco;
- autenticação;
- validações;
- testes;
- integrações externas;

colocar tudo em `main.py` rapidamente se torna difícil de manter.

Uma organização melhor separa responsabilidades.

---

# 3. Arquitetura de software

Arquitetura é a forma como estruturamos um sistema:

- quais são seus componentes;
- quais responsabilidades cada componente possui;
- como eles se comunicam;
- quais dependências existem entre eles.

Não existe uma única arquitetura correta.

A escolha depende do tamanho, domínio e necessidades do sistema.

---

## 3.1 Arquitetura em Camadas

Uma das abordagens mais comuns é separar o sistema em camadas.

```text
┌─────────────────────────┐
│      Apresentação       │
│    API / Endpoints      │
├─────────────────────────┤
│      Aplicação          │
│    Casos de uso         │
├─────────────────────────┤
│       Domínio           │
│     Regras de negócio   │
├─────────────────────────┤
│    Infraestrutura       │
│ Banco / serviços externos│
└─────────────────────────┘
```

Exemplo:

```text
Request
   ↓
Endpoint
   ↓
Service
   ↓
Repository
   ↓
Database
```

### Vantagens

- separação de responsabilidades;
- código mais organizado;
- facilidade para testar;
- componentes mais fáceis de substituir.

### Cuidado

Não devemos criar camadas apenas por criar.

Um projeto pequeno pode não precisar de dezenas de arquivos e abstrações.

---

# 4. Arquitetura Limpa

A **Clean Architecture** reforça a ideia de separar regras de negócio das tecnologias utilizadas.

Uma representação simplificada:

```text
        Frameworks / API / DB
                ↓
        Interface / Adapters
                ↓
          Application
                ↓
             Domain
```

A ideia principal é:

> **As regras mais importantes do sistema não devem depender diretamente de detalhes externos.**

Por exemplo, uma regra de negócio não deveria precisar saber se os dados estão sendo armazenados em PostgreSQL, SQLite ou outro banco.

### Quando faz sentido?

É especialmente útil quando:

- o domínio possui regras complexas;
- o sistema tende a crescer;
- existem várias integrações;
- testabilidade e manutenção são importantes.

Para aplicações pequenas, aplicar toda a estrutura de Clean Architecture pode gerar complexidade desnecessária.

---

# 5. Outras arquiteturas importantes

Não precisamos decorar uma lista de arquiteturas. O importante é reconhecer diferentes formas de organizar sistemas.

### Monólito

Todo o sistema é desenvolvido e implantado como uma aplicação.

```text
┌──────────────────────┐
│      Aplicação       │
│ API + regras + DB    │
└──────────────────────┘
```

Monólito **não significa código desorganizado**.

Um monólito pode ser muito bem estruturado internamente.

### SPA — Single Page Application

Aplicações web nas quais o frontend executa grande parte da navegação e interação no navegador, consumindo APIs.

```text
Browser
   │
   ├── JavaScript / UI
   │
   ↓
  API
   ↓
Backend
```

### SOA — Service-Oriented Architecture

Organiza funcionalidades como serviços relativamente independentes, que se comunicam por contratos bem definidos.

```text
            ┌── Serviço A
Cliente ────┼── Serviço B
            └── Serviço C
```

SOA e microsserviços possuem conceitos relacionados, mas não são sinônimos.

> **Para esta disciplina:** o objetivo é reconhecer essas abordagens e entender seus trade-offs, não implementar todas elas.

---

# 6. Organização de um projeto FastAPI

Para nosso projeto, podemos começar a sair do `main.py` único.

Uma estrutura possível:

```text
backend/
├── app/
│   ├── main.py
│   ├── api/
│   │   └── routes/
│   │       └── users.py
│   ├── schemas/
│   │   └── user.py
│   └── services/
│       └── user.py
│
├── tests/
├── pyproject.toml
└── poetry.lock
```

A estrutura pode evoluir posteriormente com:

```text
repositories/
models/
database/
core/
```

O importante é que cada parte tenha uma responsabilidade clara.

---

# 7. APIs: revisão rápida

Uma **API** define uma forma de comunicação entre sistemas.

Em uma API HTTP, normalmente trabalhamos com:

| Método | Uso comum |
|---|---|
| `GET` | Consultar |
| `POST` | Criar |
| `PUT` | Substituir/atualizar |
| `PATCH` | Atualizar parcialmente |
| `DELETE` | Remover |

Exemplo:

```text
GET    /users
GET    /users/10
POST   /users
PUT    /users/10
DELETE /users/10
```

---

## 7.1 Endpoint

Um endpoint é um ponto de acesso da API.

Ele normalmente é definido por:

```text
MÉTODO + CAMINHO
```

Por exemplo:

```text
GET /users/10
```

O cliente envia uma requisição e o servidor produz uma resposta.

```text
Cliente
   │
   │ GET /users/10
   ↓
FastAPI
   │
   │ JSON
   ↓
Cliente
```

---

# 8. Primeiro endpoint com FastAPI

Instalação:

```bash
poetry add fastapi uvicorn
```

Exemplo:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "API funcionando!"}
```

Executando:

```bash
poetry run uvicorn app.main:app --reload
```

A API estará disponível em:

```text
http://localhost:8000
```

E a documentação automática em:

```text
http://localhost:8000/docs
```

---

# 9. Path Parameters

Podemos receber informações diretamente na URL:

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

Requisição:

```text
GET /users/10
```

Resposta:

```json
{
  "user_id": 10
}
```

O FastAPI utiliza a anotação `int` para validar o parâmetro.

---

# 10. Query Parameters

Também podemos receber parâmetros de consulta:

```python
@app.get("/users")
def list_users(limit: int = 10):
    return {"limit": limit}
```

Exemplo:

```text
GET /users?limit=20
```

---

# 11. POST e dados da requisição

Podemos utilizar modelos para representar os dados recebidos.

```python
from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
```

Endpoint:

```python
@app.post("/users")
def create_user(user: UserCreate):
    return user
```

Requisição:

```json
{
  "name": "Ana",
  "email": "ana@example.com"
}
```

O FastAPI/Pydantic realiza a validação dos dados.

---

# 12. Separando as rotas

Em vez de colocar todos os endpoints em `main.py`, podemos criar um router.

### `app/api/routes/users.py`

```python
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
def list_users():
    return [{"id": 1, "name": "Ana"}]
```

### `app/main.py`

```python
from fastapi import FastAPI

from app.api.routes.users import router as users_router

app = FastAPI()

app.include_router(users_router)
```

Agora:

```text
GET /users/
```

é responsabilidade do módulo de usuários.

---

# 13. Uma regra simples de organização

Ao adicionar uma funcionalidade, pergunte:

> **"Quem deveria ser responsável por isso?"**

Por exemplo:

```text
Endpoint
   ↓
recebe HTTP
   ↓
Service
   ↓
executa regra de negócio
   ↓
Repository
   ↓
acessa dados
```

Isso evita transformar os endpoints em funções gigantes.

---

# 14. Atividade prática

A partir do backend desenvolvido nas práticas anteriores:

### Parte 1 — Organização

Crie uma estrutura semelhante a:

```text
app/
├── main.py
├── api/
│   └── routes/
├── schemas/
└── services/
```

### Parte 2 — API

Crie endpoints para um recurso simples do projeto.

Exemplo:

```text
GET    /items
GET    /items/{id}
POST   /items
```

### Parte 3 — Validação

Crie um modelo Pydantic:

```python
class ItemCreate(BaseModel):
    name: str
    description: str | None = None
```

### Parte 4 — Teste

Verifique os endpoints em:

```text
http://localhost:8000/docs
```

E mantenha os testes automatizados criados na Prática 3.

---

# 15. Checklist da prática

Ao final da aula, o projeto deve ter:

- [ ] uma estrutura de pastas organizada;
- [ ] `main.py` responsável pela inicialização da aplicação;
- [ ] rotas separadas em módulos;
- [ ] pelo menos um `GET`;
- [ ] pelo menos um `POST`;
- [ ] uso de Path ou Query Parameters;
- [ ] pelo menos um modelo Pydantic;
- [ ] testes anteriores continuando a passar.

---

# 16. O que fica para as próximas práticas?

Nesta prática, o foco é **estrutura + API**.

Ainda não precisamos resolver toda a persistência.

Na próxima etapa:

```text
FastAPI
   ↓
Arquitetura
   ↓
PostgreSQL
   ↓
SQLAlchemy
   ↓
Migrations
```

A ideia é evoluir o mesmo projeto, adicionando novas responsabilidades sem perder a organização.

---

## Resumo

```text
Arquitetura
    ↓
organiza responsabilidades

API
    ↓
define como sistemas se comunicam

FastAPI
    ↓
implementa endpoints HTTP

Boa estrutura
    ↓
facilita manutenção + testes + evolução
```

> **Mensagem principal:** uma boa arquitetura não é a que possui mais pastas ou mais abstrações. É aquela que torna as responsabilidades do sistema claras e permite que ele evolua sem criar complexidade desnecessária.
