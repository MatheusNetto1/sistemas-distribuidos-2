.PHONY: help install test lint format run up up-build down build logs logs-api ps shell clean

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