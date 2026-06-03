# MoC — Map of Content: keypartner_app
> Карта проекта. Единая точка входа для понимания структуры, правил и источников.
> Обновлять при добавлении новых документов или изменении правил.

---

## Что это за проект

**Тема ВКР:** «Автоматизация процесса взаимодействия с клиентами в ООО "Ки Партнер ИТ" с использованием веб-сервиса для централизованного управления заявками»

**Стек:** Python / Django 5.x · PostgreSQL · WhiteNoise · Gunicorn · GitFlic · Render/PythonAnywhere

**Период практики:** 11.05.2026 – 07.06.2026 · Дедлайн кода: 05.06.2026 · Сдача в ЭИОС: до 09.06.2026

---

## Иерархия источников истины

Приоритет убывает сверху вниз. При конфликте — побеждает более высокий.

| Приоритет | Источник | Файл | Что регулирует |
|---|---|---|---|
| 1 | **ИЗ преподавателя** | `uploads/17. Люлюкин_ИЗ.docx` (строки 115–124) | Жёсткие требования: страницы, меню, роли, ЛК, БД, код |
| 2 | **Балльная шкала (TZ_CHECKLIST)** | `docs/TZ_CHECKLIST.md` | 19 критериев, 57 баллов — всё нужно закрыть |
| 3 | **Шаблон отчёта** | `uploads/ОТЧЁТ...16052026.md` | Структура отчёта, ориентир по содержанию разделов (DeepSeek-драфт, можно адаптировать) |
| 4 | **Технический протокол** | `docs/DEV_PROTOCOL.md` | Правила разработки, порядок коммита, hardcode-запреты |
| 5 | **Конвенция коммитов** | `COMMIT_CONVENTIONS.md` | Формат ВКР-NNN, язык, changelog |

---

## Карта документов проекта

### Протокол и правила
- `docs/DEV_PROTOCOL.md` — протокол разработки: Phase 1/2/3, источники сверки а–ж, запреты hardcode
- `COMMIT_CONVENTIONS.md` — соглашения по коммитам: формат ВКР-NNN, нумерация, правила

### Трекер прогресса
- `docs/TZ_CHECKLIST.md` — живая таблица: 19 критериев балльной шкалы, текущий счёт, блокеры
- `README.md` — changelog по неделям (обновляется только при закрытии недели)
- `RELEASE_NOTES.md` — детальный changelog: каждый релиз prepend

### Аналитика и требования
- `docs/1.3_Analiz_IT_Infrastruktury.md` — ИТ-инфраструктура ООО «Ки Партнер ИТ»
- `docs/1.4_Analiz_Trebovaniy_Polzovateley.md` — требования F01–F14 для 3 ролей
- `docs/2.1_Color_Typography.md` — дизайн-система: токены, Inter, WCAG AA

### Диаграммы
- `docs/diagrams/AS_IS_Activity_Diagram.drawio` + `.png` — бизнес-процесс AS IS
- `docs/diagrams/TO_BE_Activity_Diagram.drawio` + `.png` — бизнес-процесс TO BE
- `docs/diagrams/ER_*` — три уровня ER: инфологическая, логическая, физическая

### DevLog (история решений)
- `docs/DevLog_ВКР-025-030_2026-05-25-26.md`
- `docs/DevLog_ВКР-031-032_2026-05-27.md`
- `docs/DevLog_ВКР-033_2026-05-28.md`
- `docs/DevLog_ВКР-034_2026-05-28.md`
- `docs/DevLog_ВКР-035_2026-05-29.md`
- `docs/DevLog_ВКР-036_2026-05-29.md`
- `docs/DevLog_ВКР-037_2026-05-29.md`
- `docs/DevLog_ВКР-038_2026-06-01.md`

---

## Как работает цикл разработки

```
Phase 1 — Анализ
  Сверка с источниками а–ж:
  а) Диаграммы (AS IS / TO BE / ER)
  б) Дизайн-доки (2.1_Color_Typography)
  в) Кодовая база (base.html, views.py, models.py, urls.py)
  г) ТЗ / 1.4 (F01–F14)
  д) README / план недели
  е) TZ_CHECKLIST (балльная шкала)
  ж) ИЗ преподавателя (жёсткие требования)

Phase 2 — План
  → СТОП, ждём подтверждения

Phase 3 — Код
  → Проверки: AST · URL-теги · hardcode · HEX
  → DevLog_ВКР-NNN
  → RELEASE_NOTES prepend
  → TZ_CHECKLIST обновить
  → README — только при закрытии недели
```

---

## Текущий статус (обновлять вручную)

| Неделя | Период | Статус |
|---|---|---|
| Неделя 1 | 11–17 мая | готово — Анализ предметной области |
| Неделя 2 | 18–24 мая | готово — Проектирование (ER, SQL, дизайн) |
| Неделя 3 | 25–31 мая | готово — Django, 10 публ. страниц, ЛК клиент |
| Неделя 4 | 1–7 июня | в работе — ЛК менеджер, экспорт, деплой |

**Коммитов:** 47 / 50 — после пуша ВКР-046 и ВКР-047 сегодня (03.06)
**Баллов:** 52 / 57

---

## Что запушить сегодня (03.06, среда)

Команды готовы — скопировать и выполнить в терминале:

```bash
cd /Users/displayboy/Library/Mobile\ Documents/iCloud\~md\~obsidian/Documents/Vault/01_PROJECTS/MUIV_Practice_2026/keypartner_app

git add core/views.py core/urls.py \
        templates/core/manager_dashboard.html \
        templates/core/manager_ticket_detail.html \
        static/css/style.css RELEASE_NOTES.md \
        docs/DevLog_ВКР-046_2026-06-03.md \
        docs/TZ_CHECKLIST.md
git commit -m "ВКР-046: экспорт заявок в .xlsx и .docx
- export_tickets_xlsx_view: все заявки → .xlsx
- export_ticket_docx_view: карточка заявки → .docx
- manager_dashboard: кнопка Скачать список (.xlsx)
- manager_ticket_detail: кнопка Скачать карточку (.docx)
- CSS: .export-bar, .ticket-detail__footer"

git add render.yaml build.sh runtime.txt \
        keypartner/settings.py \
        docs/TEST_PLAN.md \
        RELEASE_NOTES.md \
        docs/DevLog_ВКР-047_2026-06-04.md
git commit -m "ВКР-047: деплой-конфиг Render + тест-план
- render.yaml: web-сервис + PostgreSQL free tier
- build.sh: install → collectstatic → migrate → seed roles
- runtime.txt: Python 3.11
- settings.py: CSRF_TRUSTED_ORIGINS
- docs/TEST_PLAN.md: 14 тест-кейсов, 3 баг-репорта"

git push
```

---

## Что делать в четверг 04.06

1. **Деплой на Render** — render.com → New → Blueprint → подключить репозиторий GitFlic
2. После деплоя добавить env: `CSRF_TRUSTED_ORIGINS=https://<имя>.onrender.com`
3. В Shell на Render: `python manage.py createsuperuser`
4. Создать тестовые данные через /admin/: 3 пользователя (admin/manager/client), услуги, приоритеты
5. **ВКР-048**: дамп БД → `docs/db_dump.sql`

```bash
# Команда для дампа (credentials взять из Render Dashboard → DB → Connection)
pg_dump "postgresql://keypartner:<pass>@<host>/keypartner_db" > docs/db_dump.sql
git add docs/db_dump.sql README.md
git commit -m "ВКР-048: дамп PostgreSQL + ссылка на сайт в README"
git push
```

---

## Что делать в пятницу 05.06

1. Сделать скриншоты всех 10 публичных страниц + ЛК клиента + ЛК менеджера
2. Сохранить в `docs/screenshots/` (имена: `01_home.png`, `02_about.png`, ...)
3. Вставить скриншоты в отчёт на места `⟨СКРИН: ...⟩`
4. Вставить URL сайта в раздел 1.1 отчёта
5. **ВКР-049**: скриншоты в репозиторий

```bash
git add docs/screenshots/ docs/MoC_Project.md
git commit -m "ВКР-049: скриншоты интерфейса + обновлён MoC"
git push
```

6. **ВКР-050**: финальный README

```bash
git add README.md RELEASE_NOTES.md
git commit -m "ВКР-050: финальный README — ссылка на сайт, итоги недели 4"
git push
```

После этого: **50 коммитов**, сайт работает, отчёт готов к сдаче в ЭИОС.

---

## Жёсткие требования ИЗ — статус

| Требование | Статус |
|---|---|
| ≥10 страниц (неавторизованный) | готово (ВКР-037) |
| Макет каждой страницы | скриншоты после деплоя (пятница) |
| ≥10 пунктов меню + breadcrumbs | готово (ВКР-037) |
| БД ≥10 таблиц, PostgreSQL | готово — 14 таблиц (ВКР-029) |
| Дамп БД в репозитории | четверг после деплоя |
| ≥3 роли | готово — admin/manager/client (ВКР-029) |
| Панель администратора ≥5 страниц | готово — Django admin, 14 моделей (ВКР-028) |
| Личный кабинет ≥5 страниц | готово — 5 клиент + 5 менеджер (ВКР-041/044) |
| Доступ к файловой системе | готово (ВКР-045) |
| Формирование .docx / .xlsx | готово (ВКР-046) |
| ≥2000 строк кода | в работе — проверить: grep -v '^\s*$' **/*.py \| wc -l |
| ≥50 коммитов | 47/50 — осталось 3 (чт-пт) |
| Сайт на хостинге | четверг |
