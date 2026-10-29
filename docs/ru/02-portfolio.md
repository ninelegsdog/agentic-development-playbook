> Назад: [оглавление](00-index.md)

# 1. Что лежит в портфолио (доказательная база)

| Проект | Назначение | Тестов | Проходит |
|---|---|---:|---:|
| [`botkit-bookingbot`](https://github.com/ninelegsdog/botkit-bookingbot) | запись и бронирование, оплата ЮKassa | 185 | 179 |
| [`botkit-leadgen`](https://github.com/ninelegsdog/botkit-leadgen) | сбор и квалификация лидов | 105 | 102 |
| [`botkit-store`](https://github.com/ninelegsdog/botkit-store) | каталог, корзина, заказ | 171 | 168 |
| [`botkit-support`](https://github.com/ninelegsdog/botkit-support) | обращения, тикеты, SLA | 197 | 194 |
| [`botkit-membership`](https://github.com/ninelegsdog/botkit-membership) | подписки, оплата, доступ | 197 | 194 |
| [`botkit-reminder`](https://github.com/ninelegsdog/botkit-reminder) | напоминания и рассылки | 170 | 167 |
| [`botkit-docuflow`](https://github.com/ninelegsdog/botkit-docuflow) | документы, генерация PDF | 156 | 150 |
| [`botkit-pricesentry`](https://github.com/ninelegsdog/botkit-pricesentry) | мониторинг цен, алерты | 111 | 110 |
| [`botkit-delivery`](https://github.com/ninelegsdog/botkit-delivery) | статусы доставки, webhook | 147 | 141 |
| [`botkit-core`](https://github.com/ninelegsdog/botkit-core) | общая библиотека девяти ботов | 98 | 94 |
| [`botkit-monitoring`](https://github.com/ninelegsdog/botkit-monitoring) | наблюдаемость: Prometheus, Grafana, Loki, Tempo, Alertmanager, OTel, MinIO | — | — |

**Итого 1 439 тестов** [E:tests.bots] в девяти ботах (1 405 проходят, 34 пропущены) плюс 98 в общей
библиотеке `botkit-core` (94 проходят, 4 пропущены): **1 537 собранных, 1 499
проходящих, 38 пропущенных** [E:tests.total]. Девять ботов работают в продакшене (webhook, TLS,
health-check, автоперезапуск) [E:bots.count].

Инфраструктура, которую я собрал вокруг них: CI/CD (lint → test → deploy → rollback),
наблюдаемость из 10 сервисов в `botkit-monitoring` [E:infra.services], бэкапы с проверкой целостности,
gitleaks-гейт в CI ботов.

---
---

[← Оглавление](00-index.md) · [← Почему этот документ существует](01-why.md) · [2. Архитектура harness →](03-harness.md)

