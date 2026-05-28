"""
Модели веб-сервиса Key Partner — управление заявками клиентов.
Требования: F01–F14 (1.4_Analiz_Trebovaniy_Polzovateley.md)
СУБД: PostgreSQL
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# ─── Справочники ────────────────────────────────────────────────────────────

class Role(models.Model):
    """Роли пользователей: admin, manager, client (F12)"""
    name        = models.CharField(max_length=50, unique=True, verbose_name='Роль')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    class Meta:
        db_table = 'role'
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return self.name


class Priority(models.Model):
    """Приоритеты заявок: low, medium, high, critical (F14)"""
    name        = models.CharField(max_length=50, unique=True, verbose_name='Название')
    level       = models.IntegerField(verbose_name='Уровень приоритета')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    class Meta:
        db_table = 'priority'
        verbose_name = 'Приоритет'
        verbose_name_plural = 'Приоритеты'
        ordering = ['level']

    def __str__(self):
        return self.name


class Category(models.Model):
    """Категории услуг и статей (F14)"""
    name        = models.CharField(max_length=100, verbose_name='Название')
    slug        = models.SlugField(max_length=100, unique=True, verbose_name='Slug')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    class Meta:
        db_table = 'category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Теги для статей базы знаний"""
    name = models.CharField(max_length=100, verbose_name='Тег')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Slug')

    class Meta:
        db_table = 'tag'
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


# ─── Пользователи ───────────────────────────────────────────────────────────

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        role_admin = Role.objects.get_or_create(name='admin')[0]
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', role_admin)
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Учётные записи пользователей (F01, F11, F12)"""
    role       = models.ForeignKey(
                     Role, on_delete=models.RESTRICT,
                     default=3, verbose_name='Роль'
                 )
    username   = models.CharField(max_length=150, unique=True, verbose_name='Логин')
    email      = models.EmailField(max_length=254, unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=100, default='', verbose_name='Имя')
    last_name  = models.CharField(max_length=100, default='', verbose_name='Фамилия')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    is_active  = models.BooleanField(default=True, verbose_name='Активен')
    is_staff   = models.BooleanField(default=False, verbose_name='Сотрудник')

    objects = UserManager()

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        indexes = [
            models.Index(fields=['role']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f'{self.username} ({self.role})'

    @property
    def is_admin(self):
        return self.role.name == 'admin'

    @property
    def is_manager(self):
        return self.role.name == 'manager'

    @property
    def is_client(self):
        return self.role.name == 'client'


# ─── Услуги ─────────────────────────────────────────────────────────────────

class Service(models.Model):
    """Каталог услуг компании"""
    category    = models.ForeignKey(
                      Category, on_delete=models.RESTRICT,
                      verbose_name='Категория'
                  )
    title       = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    is_active   = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        db_table = 'service'
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        indexes = [models.Index(fields=['category'])]

    def __str__(self):
        return self.title


# ─── Заявки ─────────────────────────────────────────────────────────────────

class Project(models.Model):
    """Заявки клиентов — основная сущность (F02, F03, F06, F07, F08)"""

    STATUS_NEW         = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_RESOLVED    = 'resolved'
    STATUS_CLOSED      = 'closed'
    STATUS_CANCELLED   = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_NEW,         'Новая'),
        (STATUS_IN_PROGRESS, 'В работе'),
        (STATUS_RESOLVED,    'Решена'),
        (STATUS_CLOSED,      'Закрыта'),
        (STATUS_CANCELLED,   'Отменена'),
    ]

    # Статусы заявок, показываемых в публичном портфолио (ВКР-034)
    PORTFOLIO_STATUSES = [STATUS_RESOLVED, STATUS_CLOSED]

    user        = models.ForeignKey(
                      User, on_delete=models.RESTRICT,
                      related_name='tickets', verbose_name='Клиент'
                  )
    service     = models.ForeignKey(
                      Service, on_delete=models.RESTRICT,
                      verbose_name='Услуга'
                  )
    manager     = models.ForeignKey(
                      User, on_delete=models.SET_NULL,
                      null=True, blank=True,
                      related_name='managed_tickets', verbose_name='Менеджер'
                  )
    priority    = models.ForeignKey(
                      Priority, on_delete=models.RESTRICT,
                      default=2, verbose_name='Приоритет'
                  )
    title       = models.CharField(max_length=255, verbose_name='Тема')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    status      = models.CharField(
                      max_length=50, choices=STATUS_CHOICES,
                      default=STATUS_NEW, verbose_name='Статус'
                  )
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    updated_at  = models.DateTimeField(auto_now=True, verbose_name='Обновлена')

    class Meta:
        db_table = 'project'
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['manager']),
            models.Index(fields=['priority']),
            models.Index(fields=['status']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f'#{self.pk} — {self.title} [{self.status}]'


# ─── Контент сайта ──────────────────────────────────────────────────────────

class News(models.Model):
    """Новостная лента"""
    author       = models.ForeignKey(
                       User, on_delete=models.RESTRICT,
                       verbose_name='Автор'
                   )
    title        = models.CharField(max_length=255, verbose_name='Заголовок')
    content      = models.TextField(verbose_name='Содержание')
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата публикации')

    class Meta:
        db_table = 'news'
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['author']),
            models.Index(fields=['-published_at']),
        ]

    def __str__(self):
        return self.title


class Article(models.Model):
    """Статьи базы знаний"""
    category     = models.ForeignKey(
                       Category, on_delete=models.RESTRICT,
                       verbose_name='Категория'
                   )
    author       = models.ForeignKey(
                       User, on_delete=models.RESTRICT,
                       verbose_name='Автор'
                   )
    tags         = models.ManyToManyField(
                       Tag, through='ArticleTag',
                       blank=True, verbose_name='Теги'
                   )
    title        = models.CharField(max_length=255, verbose_name='Заголовок')
    content      = models.TextField(verbose_name='Содержание')
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата публикации')
    is_published = models.BooleanField(default=False, verbose_name='Опубликована')

    class Meta:
        db_table = 'article'
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['author']),
        ]

    def __str__(self):
        return self.title


class ArticleTag(models.Model):
    """M:N — Теги статей"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    tag     = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = 'article_tag'
        unique_together = [('article', 'tag')]
        indexes = [
            models.Index(fields=['article']),
            models.Index(fields=['tag']),
        ]


# ─── Коммуникация ───────────────────────────────────────────────────────────

class ContactMessage(models.Model):
    """Форма обратной связи (анонимные и авторизованные обращения)"""
    user         = models.ForeignKey(
                       User, on_delete=models.SET_NULL,
                       null=True, blank=True, verbose_name='Пользователь'
                   )
    name         = models.CharField(max_length=100, verbose_name='Имя')
    email        = models.EmailField(max_length=254, verbose_name='Email')
    phone        = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон')
    subject      = models.CharField(max_length=255, verbose_name='Тема')
    message      = models.TextField(verbose_name='Сообщение')
    created_at   = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    is_processed = models.BooleanField(default=False, verbose_name='Обработано')

    class Meta:
        db_table = 'contact_message'
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'
        ordering = ['-created_at']
        indexes = [models.Index(fields=['user'])]

    def __str__(self):
        return f'{self.subject} — {self.name}'


class Comment(models.Model):
    """Комментарии к заявке (F05, F07, F09)"""
    project    = models.ForeignKey(
                     Project, on_delete=models.CASCADE,
                     related_name='comments', verbose_name='Заявка'
                 )
    user       = models.ForeignKey(
                     User, on_delete=models.RESTRICT,
                     verbose_name='Автор'
                 )
    text       = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    is_edited  = models.BooleanField(default=False, verbose_name='Отредактировано')

    class Meta:
        db_table = 'comment'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['project']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f'Комментарий #{self.pk} к заявке #{self.project_id}'


class Attachment(models.Model):
    """Вложения к заявке (F02, F07)"""
    project   = models.ForeignKey(
                    Project, on_delete=models.CASCADE,
                    related_name='attachments', verbose_name='Заявка'
                )
    filename  = models.CharField(max_length=255, verbose_name='Имя файла')
    file_path = models.CharField(max_length=500, verbose_name='Путь к файлу')
    file_type = models.CharField(max_length=50, verbose_name='Тип файла')
    file_size = models.IntegerField(verbose_name='Размер (байт)')

    class Meta:
        db_table = 'attachment'
        verbose_name = 'Вложение'
        verbose_name_plural = 'Вложения'
        indexes = [models.Index(fields=['project'])]

    def __str__(self):
        return self.filename


class Notification(models.Model):
    """Уведомления пользователей (F04)"""
    user       = models.ForeignKey(
                     User, on_delete=models.CASCADE,
                     related_name='notifications', verbose_name='Пользователь'
                 )
    project    = models.ForeignKey(
                     Project, on_delete=models.CASCADE,
                     null=True, blank=True, verbose_name='Заявка'
                 )
    message    = models.TextField(verbose_name='Сообщение')
    is_read    = models.BooleanField(default=False, verbose_name='Прочитано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        db_table = 'notification'
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['project']),
            models.Index(fields=['is_read']),
        ]

    def __str__(self):
        return f'Уведомление для {self.user} — {"прочитано" if self.is_read else "новое"}'
