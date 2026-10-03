.PHONY: help install test lint format run up up-build down build logs logs-api ps shell clean db-upgrade db-downgrade db-current db-history db-migration db-psql

POETRY := poetry -C backend
PYTEST := $(POETRY) run pytest
RUFF := $(POETRY) run ruff
UVICORN := $(POETRY) run uvicorn

help:
	@echo "Comandos disponiveis:"
	@echo "  make install  - instala as dependencias do backend"
	@echo "  make test     - executa os testes"
	@echo "  make lint     - verifica o codigo com Ruff"
	@echo "  make format   - formata o codigo com Ruff"
	@echo "  make run      - inicia o backend localmente"
	@echo "  make up       - sobe os containers"
	@echo "  make up-build - reconstroi a imagem e sobe os containers"
	@echo "  make down     - para e remove os containers"
	@echo "  make build    - constroi as imagens"
	@echo "  make logs     - acompanha os logs"
	@echo "  make logs-api - acompanha apenas os logs da API"
	@echo "  make ps       - mostra o status dos serviços"
	@echo "  make shell    - abre um shell no container da API"
	@echo "  make clean    - remove containers, rede e volumes do Compose"
	@echo "  make db-upgrade   - aplica as migrations pendentes (Alembic)"
	@echo "  make db-downgrade - desfaz a ultima migration"
	@echo "  make db-current   - mostra a versao atual do banco"
	@echo "  make db-history   - lista o historico de migrations"
	@echo "  make db-migration MSG=\"descricao\" - gera uma nova migration"
	@echo "  make db-psql      - abre o psql no container do PostgreSQL"

install:
	$(POETRY) install

test:
	$(PYTEST)

lint:
	$(RUFF) check .

format:
	$(RUFF) format .

run:
	$(UVICORN) app.main:app --reload

up:
	docker compose up -d

up-build:
	docker compose up -d --build

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f

logs-api:
	docker compose logs -f api

ps:
	docker compose ps

shell:
	docker compose exec api sh

clean:
	docker compose down -v

db-upgrade:
	docker compose exec api alembic upgrade head

db-downgrade:
	docker compose exec api alembic downgrade -1

db-current:
	docker compose exec api alembic current

db-history:
	docker compose exec api alembic history

db-migration:
	@test -n "$(MSG)" || (echo "Uso: make db-migration MSG=\"descricao\"" && exit 1)
	docker compose run --rm -v "$(CURDIR)/backend/alembic/versions:/app/alembic/versions" api alembic revision --autogenerate -m "$(MSG)"

db-psql:
	docker compose exec db sh -c 'psql -U $$POSTGRES_USER -d $$POSTGRES_DB'
