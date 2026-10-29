# Agentic Development Playbook


[![License](https://img.shields.io/github/license/ninelegsdog/agentic-development-playbook.svg)](LICENSE)
[![CI](https://github.com/ninelegsdog/agentic-development-playbook/actions/workflows/ci.yml/badge.svg)](https://github.com/ninelegsdog/agentic-development-playbook/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/ninelegsdog/agentic-development-playbook.svg)](https://github.com/ninelegsdog/agentic-development-playbook/releases)

## Contents

- [What this is](#what-this-is)
- [TL;DR (EN)](#tldr-en)
- [Почему этот документ существует](#почему-этот-документ-существует)
- [1. Что лежит в портфолио (доказательная база)](#1-что-лежит-в-портфолио-доказательная-база)
- [2. Архитектура harness](#2-архитектура-harness)
  - [Что даёт harness](#что-даёт-harness)
- [3. Принципы работы с контекстом](#3-принципы-работы-с-контекстом)
- [4. Шаблон `AGENTS.md`](#4-шаблон-agentsmd)
- [5. Пример спецификации задачи](#5-пример-спецификации-задачи)
- [6. Чек-лист ревью AI-кода](#6-чек-лист-ревью-ai-кода)
- [7. Чек-лист безопасности секретов](#7-чек-лист-безопасности-секретов)
- [8. Цикл тестирования и исправления](#8-цикл-тестирования-и-исправления)
  - [Честная оговорка о покрытии](#честная-оговорка-о-покрытии)
- [9. Передача контекста между агентами](#9-передача-контекста-между-агентами)
- [10. Что я не утверждаю](#10-что-я-не-утверждаю)
- [11. Контакты](#11-контакты)
- [Лицензия](#лицензия)
- [Схема harness (диаграмма)](#схема-harness-диаграмма)

> **The body of this document is in Russian.** It is a methodology write-up — the agent
> harness, context rules, the review checklists and the working rules — authored in
> Russian and kept that way rather than machine-translated into English that would
> misrepresent it. The English front page below summarises it; the Russian text is the
> document.

## What this is

How I deliver software with AI coding agents: the harness they run inside, the
context engineering that keeps a long task coherent, the review checklists for
AI-written code and secrets, and the rules an agent follows when it touches this
portfolio.

The claim it argues is specific and falsifiable: the quality of agent-produced
code is a property of the harness and the acceptance criteria, not of the model.
A documented case study follows — nine Telegram bots, each with its own
repository, CI and production deployment.

**Short version:** implementation code in these projects is produced by AI coding
agents inside a harness I design — requirements, constraints, acceptance
criteria, context budget, tests and review gates. I own the process and the
result. Below is that process, written down, with the numbers that prove it runs.

---

## TL;DR (EN)

How I ship software with AI coding agents: **harness design, context engineering, strict quality gates, and verification discipline**.

- **Scale:** 9 production Telegram bots, 1,537 tests (1,439 bots + 98 core), full observability stack
- **Key insight:** Agent output quality depends on the **harness + acceptance criteria + gates**, not the model choice
- **Approach:** Specification → Context/AGENTS.md → Decomposition → Agent generation → Human review → Gates (lint/type/test/gitleaks) → Deploy/Verify
- **Focus:** Making agent work reproducible, reviewable, and verifiable before production
- **Structure:** English landing here; Russian canon in [docs/ru/](docs/ru/00-index.md); reusable templates in [templates/](templates/README.md)

**Where the numbers come from.** Test counts and coverage were measured on
2026-10-28 at the commits recorded in [`evidence/metrics.json`](evidence/metrics.json);
the reproduction command is in [`evidence/README.md`](evidence/README.md). A number
that is self-reported rather than reproduced is marked **E3**; planned work is
marked **E4**.

> The full methodology (in Russian) follows below.


---

> **Русский канон переехал в [`docs/ru/`](docs/ru/00-index.md).** Ниже — compat-заголовки,
> чтобы старые ссылки на якоря продолжали работать; полный текст — по ссылке.

## Почему этот документ существует

Полная глава — в [`docs/ru/01-why.md`](docs/ru/01-why.md).

## 1. Что лежит в портфолио (доказательная база)

Полная глава — в [`docs/ru/02-portfolio.md`](docs/ru/02-portfolio.md).

## 2. Архитектура harness

Полная глава — в [`docs/ru/03-harness.md`](docs/ru/03-harness.md).

### Что даёт harness

См. [`docs/ru/03-harness.md`](docs/ru/03-harness.md#что-даёт-harness).

## 3. Принципы работы с контекстом

Полная глава — в [`docs/ru/04-context.md`](docs/ru/04-context.md).

## 4. Шаблон `AGENTS.md`

Полная глава — в [`docs/ru/05-agents-template.md`](docs/ru/05-agents-template.md).

## 5. Пример спецификации задачи

Полная глава — в [`docs/ru/06-spec.md`](docs/ru/06-spec.md).

## 6. Чек-лист ревью AI-кода

Полная глава — в [`docs/ru/07-review.md`](docs/ru/07-review.md).

## 7. Чек-лист безопасности секретов

Полная глава — в [`docs/ru/08-secrets.md`](docs/ru/08-secrets.md).

## 8. Цикл тестирования и исправления

Полная глава — в [`docs/ru/09-testing-cycle.md`](docs/ru/09-testing-cycle.md).

### Честная оговорка о покрытии

См. [`docs/ru/09-testing-cycle.md`](docs/ru/09-testing-cycle.md#честная-оговорка-о-покрытии).

## 9. Передача контекста между агентами

Полная глава — в [`docs/ru/10-handoff.md`](docs/ru/10-handoff.md).

## Handoff

Полный шаблон — в [`docs/ru/10-handoff.md`](docs/ru/10-handoff.md#handoff).

## 10. Что я не утверждаю

Полная глава — в [`docs/ru/11-not-claiming.md`](docs/ru/11-not-claiming.md).

## 11. Контакты

Полная глава — в [`docs/ru/12-contacts.md`](docs/ru/12-contacts.md).

## Схема harness (диаграмма)

Полная диаграмма — в [`docs/ru/03-harness.md`](docs/ru/03-harness.md#схема-harness-диаграмма).

## Лицензия

MIT

