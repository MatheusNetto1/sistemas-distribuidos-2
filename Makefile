.PHONY: help install test lint format run clean

PYTEST := poetry run pytest
UVICORN := poetry run uvicorn
RUFF := poetry run ruff

help:
	@echo "Comandos disponíveis:"
	@echo "  make install  - instala dependências"
	@echo "  make test     - executa testes"
	@echo "  make lint     - verifica o código"
	@echo "  make format   - formata o código"
	@echo "  make run      - inicia o servidor"
	@echo "  make clean    - remove arquivos temporários"

install:
	poetry install

test:
	$(PYTEST)

lint:
	$(RUFF) check .

format:
	$(RUFF) format .

run:
	$(UVICORN) app.main:app --reload