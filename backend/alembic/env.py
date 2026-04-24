from __future__ import with_statement

import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# this is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

try:  # noqa: E402
    from backend.app.models import Base
except ModuleNotFoundError:  # noqa: E402
    from app.models import Base

target_metadata = Base.metadata


def _get_sqlalchemy_url() -> str:
    url = os.getenv("GOFER_DATABASE_URL")
    if url:
        return url
    # fallback for local dev
    return "mysql+pymysql://root:root123456@127.0.0.1:3306/gofer?charset=utf8mb4"


def run_migrations_offline() -> None:
    url = _get_sqlalchemy_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = _get_sqlalchemy_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

