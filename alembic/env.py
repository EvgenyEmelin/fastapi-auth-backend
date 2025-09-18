from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy import create_engine
from alembic import context

import os
import sys

# Добавляем путь к проекту для возможности импорта моделей
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Импорт Base и модели
from app.model.base import Base  # Ваш declarative base
# Импорт всех моделей, чтобы Alembic видел все таблицы:
import app.model.user
import app.model.role
import app.model.user_role
from app.model import permission
from app.model import refresh_token
# импортируйте все модули с таблицами и моделями

# Этот объект нужен Alembic для автогенерации миграций:
target_metadata = Base.metadata

# Получаем конфиг Alembic
config = context.config

# Настройка логирования
fileConfig(config.config_file_name)

# Задайте URL подключения к вашей базе - либо из alembic.ini, либо через env переменные или конфиг
# Например, из alembic.ini:
sqlalchemy_url = config.get_main_option("sqlalchemy.url")

# Функция для запуска миграций в offline режиме (без подключения к базе)
def run_migrations_offline():
    url = sqlalchemy_url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# Функция для запуска миграций онлайн (с подключением к базе)
def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # проверять изменения типов колонок
            # include_schemas=True,   # если используете схемы в БД
        )

        with context.begin_transaction():
            context.run_migrations()

# Выбираем режим запуска миграций
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
