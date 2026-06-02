# Release Notes — Key Partner IT Web Service

---

## 🚀 Release 0.12 — UI-фиксы навигации и feature cards
📅 02.06.2026

### 🔄 Changed
- `static/css/style.css`: `white-space: nowrap` на `.nav-link` — пункты меню больше не переносятся на 2 строки
- `.nav-link`: `font-size` → `text-small`, `padding` → `space-2` — все 10 пунктов умещаются в одну строку
- `.nav-list`: `gap: 0` — убран лишний зазор
- `.site-logo`: `flex-shrink: 0` — логотип не сжимается при нехватке места
- `.feature-card`: `display: flex; flex-direction: column` — карточки одинаковой высоты

---

## 🚀 Release 0.11 — Профиль пользователя + Уведомления
📅 01.06.2026

### ✨ Added
- `core/forms.py`: `ProfileUpdateForm` — first_name/last_name/email, clean_email с защитой от чужого email (exclude self)
- `templates/core/profile.html`: боковая панель (аватар-буква, роль, дата регистрации, nav), форма редактирования, readonly логин
- `templates/core/notifications.html`: список с бейджем непрочитанных, кнопка POST «Прочитано», ссылка на заявку, empty state, пагинация
- `core/views.py`: `profile_view` GET+POST; `notifications_view` с Paginator и счётчиком unread; `notification_mark_read_view` (@require_POST, owner-check)
- `core/urls.py`: `/dashboard/profile/`, `/dashboard/notifications/`, `/dashboard/notifications/<pk>/read/`
- `static/css/style.css`: `.profile-layout` (grid 2-col), `.profile-sidebar`, `.profile-avatar`, `.profile-nav`, `.notifications-list`, `.notification-item--unread`, `.visually-hidden`

### 🔐 Security
- `notification_mark_read_view`: `@require_POST` + `get_object_or_404(..., user=request.user)` — чужое уведомление → 404
- `ProfileUpdateForm.clean_email`: `exclude(pk=self.instance.pk)` — не блокирует сохранение собственного email

### 📊 TZ_CHECKLIST
- Критерий #17б «ЛК клиента ≥5 страниц» → ✅ (было 🔄, +5 баллов)
- Счёт: 36 → **41 / 57 баллов**

---

## 🚀 Release 0.10 — Детальная страница заявки клиента
📅 01.06.2026

### ✨ Added
- `templates/core/ticket_detail.html`: шапка с бейджем статуса и мета-данными (услуга, приоритет, даты, менеджер), блок описания, список вложений (имя + тип + размер), список комментариев с автором и датой
- `core/views.py`: `ticket_detail_view` — `get_object_or_404(Project, pk=pk, user=request.user)`, `prefetch_related('comments__user', 'attachments')`
- `core/urls.py`: маршрут `/dashboard/tickets/<int:pk>/`
- `static/css/style.css`: `.ticket-detail`, `.ticket-detail__title-row`, `.ticket-meta`, `.ticket-description`, `.attachments-list`, `.attachment-item`, `.comments-list`, `.comment-card`, `.ticket-row__link`

### 🔄 Changed
- `templates/core/dashboard.html`: № и тема заявки → ссылки на `ticket_detail`

### 🔐 Security
- Клиент видит только свои заявки: фильтр `user=request.user` в `get_object_or_404` — чужая заявка возвращает 404

### 📊 TZ_CHECKLIST
- Критерий #17б «ЛК клиента ≥5 страниц» → 🔄 3/5

---

## 🚀 Release 0.9 — Дашборд клиента: список заявок + создание заявки
📅 01.06.2026

### ✨ Added
- `core/forms.py`: `ProjectCreateForm(ModelForm)` — поля title/description/service/priority; валидация `TITLE_MIN_LENGTH=5`; queryset только активных услуг
- `templates/core/ticket_create.html`: форма новой заявки — 2-col layout (service + priority), CSRF, кнопка «Отмена»
- `core/views.py`: `ticket_create_view` — GET+POST, `@login_required`, статус `STATUS_NEW` явно, redirect-after-POST
- `core/urls.py`: маршрут `/dashboard/tickets/new/`
- `static/css/style.css`: `.dashboard-header`, `.dashboard-stats`, `.stat-card`, `.stat-card--{new/progress/resolved}`, `.tickets-table`, `.ticket-row`, `.pagination`, `.ticket-form-card`, `.form-actions`

### 🔄 Changed
- `templates/core/dashboard.html`: полная перепись — заголовок + кнопка «Создать заявку», 4 stat-cards (Всего/Новых/В работе/Решено), таблица заявок с бейджами статусов, пагинация, empty state
- `core/views.py`: `dashboard_view` — полная реализация: `Project.objects.filter(user=request.user)`, `Paginator`, счётчики по статусам
- Удалён inline `style="color:..."` из старого `dashboard.html`

### 📊 TZ_CHECKLIST
- Критерий #17 «ЛК клиента ≥5 страниц» → 🔄 2/5 страниц готово

---

## 🚀 Release 0.8 — О компании, Карта сайта, детальная новость
📅 29.05.2026

### ✨ Added
- `templates/core/about.html`: страница «О компании» — hero, описание, 4 направления деятельности, 4 преимущества (Heroicons), CTA «Связаться с нами»
- `templates/core/sitemap.html`: карта сайта — структурированный список всех разделов с описаниями
- `templates/core/news_detail.html`: детальная страница новости — заголовок, дата, автор, полный текст, кнопка «← Все новости»
- `core/views.py`: `about_view`, `sitemap_view`, `news_detail_view` (с `get_object_or_404`, 404 для неопубликованных)
- `core/urls.py`: маршруты `/about/`, `/sitemap/`, `/news/<int:pk>/`
- `static/css/style.css`: `.btn-sm`, `.about-section`, `.about-list`, `.about-cta`, `.sitemap-section`, `.sitemap-list`, `.news-detail`, `.news-card__link`

### 🔄 Changed
- `templates/base.html`: добавлены «О компании» и «Карта сайта» в nav; «Личный кабинет» показывается всем (redirect для анонимных через `@login_required`)
- `templates/core/news.html`: заголовки карточек и кнопка «Читать далее →» ведут на `news_detail`

### 📊 TZ_CHECKLIST
- Критерий #8 «≥10 страниц» → ✅ (было ⚠️, +2 балла)
- Критерий #11 «≥10 пунктов меню» → ✅ (было ⚠️, +2 балла)
- Счёт: 32 → **36 / 57 баллов**

---

## 🚀 Release 0.7 — Аутентификация: логин, регистрация, 404
📅 29.05.2026

### ✨ Added
- `core/forms.py`: `LoginForm` — authenticate() в clean(), поддержка `?next=`; `RegisterForm(ModelForm)` — валидация username/email уникальности, password min 8 симв., совпадение паролей
- `templates/core/login.html`: auth-card с формой входа, non_field_errors, autofocus, next-hidden
- `templates/core/register.html`: auth-card--wide с 2-col layout, все поля User кроме role
- `templates/404.html`: страница 404 с кодом, заголовком и кнопкой «На главную»
- `static/css/style.css`: `.auth-card`, `.auth-card--wide`, `.auth-wrapper`, `.btn--full`, `.error-page`, `.error-page__code`

### 🔄 Changed
- `core/views.py`: `login_view` — GET+POST, authenticate, auth_login, redirect to ?next; `register_view` — GET+POST, Role.objects.get(name=ROLE_CLIENT), auto-login; `handler404_view` добавлен
- `keypartner/urls.py`: `handler404 = 'core.views.handler404_view'`

### 🔐 Security & Permissions
- Аутентификация через Django `authenticate()` — пароль никогда не хранится в форме
- Роль `client` присваивается явно через `Role.objects.get(name=ROLE_CLIENT)`, а не через дефолт FK
- `{% csrf_token %}` в обеих формах
- Авторизованные пользователи редиректятся с /login/ и /register/ на главную

---

## 🚀 Release 0.6 — Контакты, форма обратной связи, хлебные крошки
📅 29.05.2026

### ✨ Added
- `core/forms.py`: `ContactMessageForm(ModelForm)` — валидация name, email, phone (regex), subject, message (min 10 симв.); все ошибки именованными константами
- `core/context_processors.py`: `site_meta` — передаёт `SITE_AUTHOR` во все шаблоны
- `templates/core/contacts.html`: page-hero + contacts-layout (реквизиты + форма), inline-ошибки, ARIA, breadcrumbs
- `static/css/style.css`: `.breadcrumb`, `.contacts-layout`, `.contacts-info__*`, `.contacts-form__*`, `.form-row` (адаптивный 2-col)

### 🔄 Changed
- `core/views.py`: `contacts_view` — GET (pre-fill для авторизованных) + POST (сохранение, redirect-after-POST, `messages.success`)
- `keypartner/settings.py`: context processor `core.context_processors.site_meta`; константа `SITE_AUTHOR` из env (ТЗ §9)
- `templates/base.html`: `{% block breadcrumbs %}` перед контентом; `{{ SITE_AUTHOR }}` в footer (ТЗ §9)
- Все 8 шаблонов: `{% block breadcrumbs %}` с хлебными крошками (ТЗ §3)

### 🔐 Security & Permissions
- `{% csrf_token %}` обязателен; POST без токена → 403
- Форма доступна всем ролям и анонимам; `user` FK заполняется только при `is_authenticated`
- Redirect-after-POST исключает double-submit

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
