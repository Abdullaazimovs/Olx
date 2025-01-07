import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Import your app's settings and database configurations
from database.models import *  # Import all models to include them in migrations
from database.db import Base
from config import settings  # Import your settings module

# This is the Alembic Config object, which provides access to .ini values
config = context.config

# Dynamically fetch the database URL from environment variables or settings
url = settings.database_url

# Update the SQLAlchemy URL in Alembic's config
config.set_main_option("sqlalchemy.url", url)

# Set up Python logging for Alembic
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Provide Alembic with access to your models' metadata for migrations
target_metadata = Base.metadata

# Define functions for running migrations offline or online
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# Check whether migrations are being run offline or online
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()