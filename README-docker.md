# Ambiente Docker

## Pré-requisitos

- Docker com Docker Compose
- Make (opcional; os comandos `docker compose` também podem ser usados diretamente)

## Configuração

Copie `.env.example` para `.env` e ajuste os valores se necessário.

```bash
cp .env.example .env
```

No Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

O `.env` não deve ser versionado.

## Subir o ambiente

```bash
make up-build
```

Ou:

```bash
docker compose up -d --build
```

A API ficará disponível em:

```text
http://localhost:8000
```

## Verificar os serviços

```bash
make ps
```

Logs:

```bash
make logs
```

Somente da API:

```bash
make logs-api
```

## Parar o ambiente

```bash
make down
```

Para remover também o volume do PostgreSQL:

```bash
make clean
```

> `make clean` apaga os dados persistidos do PostgreSQL.

## Banco de dados e migrations

O PostgreSQL sobe junto com a API. Depois de subir o ambiente, aplique as migrations:

```bash
make db-upgrade
```

Veja [docs/persistencia-postgresql-sqlalchemy.md](docs/persistencia-postgresql-sqlalchemy.md) para o fluxo completo.

## Estrutura

```text
sistemas-distribuidos-2/
├── backend/
│   ├── alembic/
│   ├── app/
│   ├── tests/
│   ├── .dockerignore
│   ├── alembic.ini
│   ├── Dockerfile
│   ├── poetry.lock
│   └── pyproject.toml
├── frontend/
├── .env.example
├── compose.yml
└── Makefile
```

O backend utiliza `./backend` como contexto de build. Dentro da rede criada pelo Compose, o PostgreSQL é acessível pelo hostname `db`.
