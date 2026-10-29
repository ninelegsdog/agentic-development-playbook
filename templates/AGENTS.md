# AGENTS.md

## Роли
- **Пользователь** = владелец продукта. Решает, что делаем.
- **Агент** = инженер + devops + tech lead. Проактивен: решает и делает,
  а не переспрашивает по каждому шагу.

## Стек
- Python 3.12+, aiogram 3.30+, SQLAlchemy 2 (async), Redis, Alembic
- pytest, ruff, mypy --strict
- Docker: user 1001:1001, read_only, cap_drop ALL, no-new-privileges

## Обязательные правила
- Строка ≤ 120 символов, PEP8, type hints везде
- Conventional Commits
- Тесты пишутся до коммита
- `ruff check .` и `mypy src/` должны проходить
- Секреты — только в `.env`; в коде их нет

## Контракты, которые нельзя вывести из кода
- <здесь перечисляются неочевидные инварианты проекта>

## Гейты перед коммитом
- ruff check . && ruff format --check .
- mypy src/
- pytest
- gitleaks protect --staged

## Где канон
- <путь> — единственный источник истины; копии каноном не являются.
