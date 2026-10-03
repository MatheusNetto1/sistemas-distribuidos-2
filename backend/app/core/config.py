import os

# Dentro do Docker Compose o host do PostgreSQL é "db" (nome do serviço).
# O valor padrão abaixo serve para execução local fora dos containers.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://app:app@localhost:5432/app",
)
