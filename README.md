# TelegramBot-Base

Шаблон TelegramBot для запуска новых проектов.

## Используемые технологии

### Aiogram

[Aiogram](https://docs.aiogram.dev/) — Python фреймворк для разработки телеграм-ботов.

### Alembic

[Alembic](https://alembic.sqlalchemy.org/en/latest/) — это легкий инструмент миграции базы данных для использования совместно с SQLAlchemy.

`alembic init -t async <change>` # это асинхронный код для создания миграций, добавьте путь для расположения директории миграции

`alembic revision --autogenerate -m "<change>` # это сгенерит миграцию, добавьте название версии миграции

`alembic upgrade head` # это обновляет/настраивает базу данных с использованием самой последней версии)

### Sqlalchemy

[Sqlalchemy](https://docs.sqlalchemy.org/) - библиотека, которая позволяет работать с реляционными базами данных с помощью ORM (объектно-реляционного сопоставления).

`alembic init -t async <change>` (это асинхронный код для создания миграций, добавьте путь для расположения директории миграции)

`alembic revision --autogenerate -m "<change>"` (это сгенерит миграцию, добавьте название версии миграции)

`alembic upgrade head` (это обновляет/настраивает базу данных с использованием самой последней версии)

### Pydantic

[Pydantic](https://docs.pydantic.dev/latest/) - библиотека Python для проверки данных и управления настройками.

### Poetry

[Poetry](https://python-poetry.org/) — это виртуальная среда, подобная venv, с более разнообразными опциями конфигурации.

### Хуки

Хуки - это скрипты, которые автоматически выполняются при наступлении определённых событий.

[Pre-commit](https://pre-commit.com/) - это фреймворк для запуска хуков (инструментов) перед созданием коммита. Pre-commit использует файл конфигурации, чтобы определить, какие хуки запускать и как их запускать.

`pip install pre-commit==3.8.0`(установить прекоммит)

`pre-commit install`(добавить прекоммит)

`pre-commit run --all-files`(запустить без коммита)

`git commit --no-verify` (пропустить выполнение хука при коммите)

### Git

[Git](https://git-scm.com/) — распределённая система управления версиями.
