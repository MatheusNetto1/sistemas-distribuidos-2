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

## Estrutura

```text
laboratorio-web/
├── backend/
│   ├── app/
│   ├── tests/
│   ├── .dockerignore
│   ├── Dockerfile
│   ├── poetry.lock
│   └── pyproject.toml
├── frontend/
├── .env.example
├── compose.yaml
└── Makefile
```

O backend utiliza `./backend` como contexto de build. Dentro da rede criada pelo Compose, o PostgreSQL é acessível pelo hostname `db`.