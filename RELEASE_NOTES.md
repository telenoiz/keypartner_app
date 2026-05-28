# Release Notes — Key Partner IT Web Service

---

## 🚀 Release 0.5 — Страницы контента
📅 28.05.2026

### ✨ Added
- `templates/core/services.html`: каталог услуг — page-hero, сетка карточек с полным описанием, empty state с CTA
- `templates/core/news.html`: лента новостей — карточки с датой и усечённым текстом, empty state
- `templates/core/projects.html`: публичное портфолио — карточки завершённых кейсов с бейджем статуса; личные данные клиентов не раскрываются
- `core/views.py`: `services_view`, `news_view`, `projects_view`; константы `SERVICES_PER_PAGE=20`, `NEWS_PER_PAGE=10`, `PROJECTS_PER_PAGE=9`
- `core/models.py`: `Project.PORTFOLIO_STATUSES = [STATUS_RESOLVED, STATUS_CLOSED]`
- `core/urls.py`: маршруты `/services/`, `/news/`, `/projects/`
- `static/css/style.css`: переменные `--badge-*` в `:root`; компоненты `.page-hero`, `.news-grid`, `.news-card`, `.projects-grid`, `.project-card`, `.badge`, `.badge--{status}`

### 🔄 Changed
- `templates/base.html`: навигация расширена — «Услуги», «Проекты», «Новости» с `aria-current`
- `templates/core/home.html`: добавлен CTA «Все услуги →» в секцию услуг

### 🔐 Security & Permissions
- Все три страницы доступны анонимным пользователям и всем ролям
- Портфолио выводит только `title`, `service.title`, `status` — поля `user` и `manager` не раскрываются

---

## 🚀 Release 0.4 — Главная страница
📅 28.05.2026

### ✨ Added
- `templates/core/home.html`: Hero-секция — заголовок, подзаголовок, адаптивный CTA по роли (аноним / авторизован)
- `templates/core/home.html`: Блок преимуществ — 4 карточки с Heroicons, контент из TO BE диаграммы и анализа AS IS
- `templates/core/home.html`: Блок услуг — выборка из БД (`Service.is_active=True`, лимит `HOME_SERVICES_COUNT`) с empty state
- `core/views.py`: константы `HOME_SERVICES_COUNT = 3`, `HOME_NEWS_COUNT = 3`
- `static/css/style.css`: компоненты `.btn-lg`, `.hero`, `.features-grid`, `.feature-card`, `.services-grid`, `.service-card`, `.empty-state`

### 🔄 Changed
- `core/views.py`: `home_view` теперь передаёт `services` и `news` в контекст шаблона

### 🔐 Security & Permissions
- Главная страница доступна всем ролям и анонимным пользователям
- CTA адаптируется на уровне шаблона через `request.user.is_authenticated` — без обращений к бэкенду

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
