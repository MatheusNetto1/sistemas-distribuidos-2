from logging.config import fileConfig

from sqlalchemy import create_engine, pool

import app.models  # noqa: F401  (registra os models em Base.metadata)
from alembic import context
from app.core.config import DATABASE_URL
from app.database.base import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata dos models: é o que o autogenerate compara com o banco.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Gera o SQL sem conectar ao banco."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Conecta ao banco indicado por DATABASE_URL e aplica as migrations."""
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
