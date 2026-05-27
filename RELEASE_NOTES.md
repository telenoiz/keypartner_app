# Release Notes — Key Partner IT Web Service

---

## 🚀 Release 0.3 — Маршруты и базовый шаблон
📅 27.05.2026

### ✨ Added
- `core/urls.py`: 6 маршрутов — `/`, `/login/`, `/register/`, `/logout/`, `/dashboard/`, `/contacts/`
- `core/views.py`: view-функции `home_view`, `login_view`, `register_view`, `logout_view`, `dashboard_view`, `contacts_view`
- `templates/base.html`: базовый шаблон — шапка, навигация, Django messages, подвал, переключатель темы
- `templates/core/`: стаб-шаблоны для всех 5 страниц (home, login, register, dashboard, contacts)
- `static/css/style.css`: дизайн-токены — цвета, типографика Inter, отступы, кнопки, формы, бейджи (WCAG AA)
- `static/css/accessible.css`: тема для слабовидящих по ГОСТ Р 52872-2012 (высокий контраст, шрифт ≥ 18px)

### 🔐 Security & Permissions
- `dashboard_view` защищён `@login_required` — неавторизованные редиректятся на `/login/?next=/dashboard/`
- `logout_view` принимает только POST (`@require_POST`) — защита от CSRF-logout через GET
- `login_view` и `register_view` редиректят авторизованных пользователей на главную

---

## 🚀 Release 0.2 — Модели, панель администратора, миграции
📅 26.05.2026

### ✨ Added
- `core/models.py`: 14 сущностей по физической ER-диаграмме — `Role`, `Priority`, `Category`, `Tag`, `User` (AbstractBaseUser), `Service`, `Project`, `News`, `Article`, `ArticleTag`, `ContactMessage`, `Comment`, `Attachment`, `Notification`
- `core/admin.py`: регистрация всех 14 моделей, инлайны Comment/Attachment, fieldsets с правами
- `core/migrations/0001_initial.py`: 14 таблиц, 21 индекс, seed-данные ролей (admin / manager / client)

---

## 🚀 Release 0.1 — Инициализация проекта
📅 25.05.2026

### ✨ Added
- Инициализация Django 5.x проекта `keypartner`
- Приложение `core` с базовой структурой
- `keypartner/settings.py`: PostgreSQL, WhiteNoise, кастомная модель пользователя (`AUTH_USER_MODEL = 'core.User'`)
- `requirements.txt`: зависимости проекта
- `.env.example`: шаблон переменных окружения
- `COMMIT_CONVENTIONS.md`: соглашения по коммитам
