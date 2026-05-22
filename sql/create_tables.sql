-- ============================================================
-- keypartner_app — Создание таблиц базы данных
-- СУБД: PostgreSQL
-- Коммит: ВКР-021
-- Требования: F01–F14 (1.4_Analiz_Trebovaniy_Polzovateley.md)
-- Дата: 2026-05-21
-- ============================================================

-- ─── Удаление таблиц (обратный порядок зависимостей) ────────

DROP TABLE IF EXISTS notification    CASCADE;
DROP TABLE IF EXISTS article_tag     CASCADE;
DROP TABLE IF EXISTS attachment      CASCADE;
DROP TABLE IF EXISTS comment         CASCADE;
DROP TABLE IF EXISTS contact_message CASCADE;
DROP TABLE IF EXISTS article         CASCADE;
DROP TABLE IF EXISTS news            CASCADE;
DROP TABLE IF EXISTS project         CASCADE;
DROP TABLE IF EXISTS service         CASCADE;
DROP TABLE IF EXISTS "user"          CASCADE;
DROP TABLE IF EXISTS category        CASCADE;
DROP TABLE IF EXISTS tag             CASCADE;
DROP TABLE IF EXISTS priority        CASCADE;
DROP TABLE IF EXISTS role            CASCADE;


-- ─── Справочники ────────────────────────────────────────────

-- Роли пользователей (F12)
CREATE TABLE role (
    id          SERIAL      PRIMARY KEY,
    name        VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);

-- Приоритеты заявок (F14)
CREATE TABLE priority (
    id          SERIAL      PRIMARY KEY,
    name        VARCHAR(50) NOT NULL UNIQUE,
    level       INTEGER     NOT NULL,
    description TEXT
);

-- Категории услуг и статей (F14)
CREATE TABLE category (
    id          SERIAL       PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    slug        VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

-- Теги статей
CREATE TABLE tag (
    id   SERIAL       PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE
);


-- ─── Пользователи ───────────────────────────────────────────

-- Учётные записи (F01, F11, F12)
-- DEFAULT role_id = 3 → 'client'
CREATE TABLE "user" (
    id            SERIAL       PRIMARY KEY,
    role_id       INTEGER      NOT NULL DEFAULT 3
                                   REFERENCES role(id) ON DELETE RESTRICT,
    username      VARCHAR(150) NOT NULL UNIQUE,
    email         VARCHAR(254) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name    VARCHAR(100) NOT NULL DEFAULT '',
    last_name     VARCHAR(100) NOT NULL DEFAULT '',
    created_at    TIMESTAMP    NOT NULL DEFAULT NOW(),
    is_active     BOOLEAN      NOT NULL DEFAULT TRUE
);

CREATE INDEX idx_user_role_id ON "user"(role_id);
CREATE INDEX idx_user_email   ON "user"(email);


-- ─── Услуги ─────────────────────────────────────────────────

-- Каталог услуг компании
CREATE TABLE service (
    id          SERIAL       PRIMARY KEY,
    category_id INTEGER      NOT NULL
                                 REFERENCES category(id) ON DELETE RESTRICT,
    title       VARCHAR(255) NOT NULL,
    description TEXT,
    is_active   BOOLEAN      NOT NULL DEFAULT TRUE
);

CREATE INDEX idx_service_category_id ON service(category_id);


-- ─── Заявки ─────────────────────────────────────────────────

-- Основная сущность системы (F02, F03, F06, F07, F08)
-- status: new → in_progress → resolved → closed | cancelled
CREATE TABLE project (
    id          SERIAL       PRIMARY KEY,
    user_id     INTEGER      NOT NULL
                                 REFERENCES "user"(id) ON DELETE RESTRICT,
    service_id  INTEGER      NOT NULL
                                 REFERENCES service(id) ON DELETE RESTRICT,
    manager_id  INTEGER
                                 REFERENCES "user"(id) ON DELETE SET NULL,
    priority_id INTEGER      NOT NULL DEFAULT 2
                                 REFERENCES priority(id) ON DELETE RESTRICT,
    title       VARCHAR(255) NOT NULL,
    description TEXT,
    status      VARCHAR(50)  NOT NULL DEFAULT 'new'
                                 CHECK (status IN (
                                     'new', 'in_progress', 'resolved',
                                     'closed', 'cancelled'
                                 )),
    created_at  TIMESTAMP    NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMP    NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_project_user_id     ON project(user_id);
CREATE INDEX idx_project_manager_id  ON project(manager_id);
CREATE INDEX idx_project_priority_id ON project(priority_id);
CREATE INDEX idx_project_status      ON project(status);
CREATE INDEX idx_project_created_at  ON project(created_at DESC);


-- ─── Контент сайта ──────────────────────────────────────────

-- Новости
CREATE TABLE news (
    id           SERIAL       PRIMARY KEY,
    author_id    INTEGER      NOT NULL
                                  REFERENCES "user"(id) ON DELETE RESTRICT,
    title        VARCHAR(255) NOT NULL,
    content      TEXT         NOT NULL,
    published_at TIMESTAMP
);

CREATE INDEX idx_news_author_id    ON news(author_id);
CREATE INDEX idx_news_published_at ON news(published_at DESC);

-- Статьи базы знаний
CREATE TABLE article (
    id           SERIAL       PRIMARY KEY,
    category_id  INTEGER      NOT NULL
                                  REFERENCES category(id) ON DELETE RESTRICT,
    author_id    INTEGER      NOT NULL
                                  REFERENCES "user"(id) ON DELETE RESTRICT,
    title        VARCHAR(255) NOT NULL,
    content      TEXT         NOT NULL,
    published_at TIMESTAMP,
    is_published BOOLEAN      NOT NULL DEFAULT FALSE
);

CREATE INDEX idx_article_category_id ON article(category_id);
CREATE INDEX idx_article_author_id   ON article(author_id);

-- Теги статей (M:N)
CREATE TABLE article_tag (
    id         SERIAL  PRIMARY KEY,
    article_id INTEGER NOT NULL
                           REFERENCES article(id) ON DELETE CASCADE,
    tag_id     INTEGER NOT NULL
                           REFERENCES tag(id) ON DELETE CASCADE,
    UNIQUE (article_id, tag_id)
);

CREATE INDEX idx_article_tag_article_id ON article_tag(article_id);
CREATE INDEX idx_article_tag_tag_id     ON article_tag(tag_id);


-- ─── Коммуникация ───────────────────────────────────────────

-- Форма обратной связи (user_id nullable — анонимные обращения)
CREATE TABLE contact_message (
    id           SERIAL       PRIMARY KEY,
    user_id      INTEGER
                                  REFERENCES "user"(id) ON DELETE SET NULL,
    name         VARCHAR(100) NOT NULL,
    email        VARCHAR(254) NOT NULL,
    phone        VARCHAR(20),
    subject      VARCHAR(255) NOT NULL,
    message      TEXT         NOT NULL,
    created_at   TIMESTAMP    NOT NULL DEFAULT NOW(),
    is_processed BOOLEAN      NOT NULL DEFAULT FALSE
);

CREATE INDEX idx_contact_message_user_id ON contact_message(user_id);

-- Комментарии к заявке (F05, F07, F09)
CREATE TABLE comment (
    id         SERIAL    PRIMARY KEY,
    project_id INTEGER   NOT NULL
                             REFERENCES project(id) ON DELETE CASCADE,
    user_id    INTEGER   NOT NULL
                             REFERENCES "user"(id) ON DELETE RESTRICT,
    text       TEXT      NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    is_edited  BOOLEAN   NOT NULL DEFAULT FALSE
);

CREATE INDEX idx_comment_project_id ON comment(project_id);
CREATE INDEX idx_comment_user_id    ON comment(user_id);

-- Вложения к заявке (F02, F07)
CREATE TABLE attachment (
    id         SERIAL       PRIMARY KEY,
    project_id INTEGER      NOT NULL
                                REFERENCES project(id) ON DELETE CASCADE,
    filename   VARCHAR(255) NOT NULL,
    file_path  VARCHAR(500) NOT NULL,
    file_type  VARCHAR(50)  NOT NULL,
    file_size  INTEGER      NOT NULL
);

CREATE INDEX idx_attachment_project_id ON attachment(project_id);

-- Уведомления (F04)
CREATE TABLE notification (
    id         SERIAL    PRIMARY KEY,
    user_id    INTEGER   NOT NULL
                             REFERENCES "user"(id) ON DELETE CASCADE,
    project_id INTEGER
                             REFERENCES project(id) ON DELETE CASCADE,
    message    TEXT      NOT NULL,
    is_read    BOOLEAN   NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_notification_user_id    ON notification(user_id);
CREATE INDEX idx_notification_project_id ON notification(project_id);
CREATE INDEX idx_notification_is_read    ON notification(is_read);


-- ─── Начальные данные (справочники) ─────────────────────────

INSERT INTO role (name, description) VALUES
    ('admin',   'Администратор системы'),
    ('manager', 'Менеджер / Сотрудник'),
    ('client',  'Клиент / Пользователь');

INSERT INTO priority (name, level, description) VALUES
    ('low',      1, 'Низкий приоритет'),
    ('medium',   2, 'Средний приоритет'),
    ('high',     3, 'Высокий приоритет'),
    ('critical', 4, 'Критический приоритет');
