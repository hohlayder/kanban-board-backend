import sys
from os.path import abspath, dirname
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

from dotenv import load_dotenv

load_dotenv()

#чтобы Python находил src/
sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))

from src.core.database import Base
from src.settings import settings

#импорт моделей для metadata
from src.models.models import User, Project, BColumn, Task, TaskLog

#объект конфигурации алембик
config = context.config

#синхронный URL + просмотр
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL_sync)
print("Alembic URL:", config.get_main_option("sqlalchemy.url"))

#логирование через alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

#функции для управления миграциями
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
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

