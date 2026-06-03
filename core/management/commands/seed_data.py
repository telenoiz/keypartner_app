"""
Management command: наполнение БД тестовыми данными.
Идемпотентна — повторный запуск не дублирует записи.

Использование:
    python manage.py seed_data
    python manage.py seed_data --no-demo-users   # только справочники
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Заполнить базу данных начальными и демонстрационными данными'

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-demo-users',
            action='store_true',
            help='Пропустить создание демо-пользователей',
        )

    def handle(self, *args, **options):
        self._seed_roles()
        self._seed_priorities()
        self._seed_categories()
        self._seed_services()
        if not options['no_demo_users']:
            self._seed_users()
        self.stdout.write(self.style.SUCCESS('Seed completed.'))

    # ── Справочники ──────────────────────────────────────────────────────────

    def _seed_roles(self):
        from core.models import Role
        for name in ('admin', 'manager', 'client'):
            _, created = Role.objects.get_or_create(name=name)
            if created:
                self.stdout.write(f'  Role created: {name}')

    def _seed_priorities(self):
        from core.models import Priority
        items = [
            ('Низкий',    1, 'Задача не срочная'),
            ('Средний',   2, 'Стандартный приоритет'),
            ('Высокий',   3, 'Требует скорейшего решения'),
            ('Критичный', 4, 'Немедленное вмешательство'),
        ]
        for name, level, desc in items:
            _, created = Priority.objects.get_or_create(
                name=name,
                defaults={'level': level, 'description': desc},
            )
            if created:
                self.stdout.write(f'  Priority created: {name}')

    def _seed_categories(self):
        from core.models import Category
        items = ['Разработка', 'Консультация', 'Техподдержка', 'Интеграция']
        for name in items:
            _, created = Category.objects.get_or_create(
                name=name,
                defaults={'slug': slugify(name, allow_unicode=False) or name.lower()},
            )
            if created:
                self.stdout.write(f'  Category created: {name}')

    def _seed_services(self):
        from core.models import Service, Category
        items = [
            ('Разработка веб-сервиса',   'Создание веб-приложений на Django/Python',        'Разработка'),
            ('IT-консультация',           'Консультации по выбору технологий и архитектуры', 'Консультация'),
            ('Техническая поддержка',     'Сопровождение и поддержка ПО',                   'Техподдержка'),
            ('Интеграция с 1С',           'Интеграция веб-сервисов с системами 1С',          'Интеграция'),
            ('Аудит безопасности',        'Проверка защищённости веб-приложений',            'Консультация'),
        ]
        for title, desc, cat_name in items:
            cat = Category.objects.filter(name=cat_name).first()
            _, created = Service.objects.get_or_create(
                title=title,
                defaults={
                    'description': desc,
                    'category': cat,
                    'is_active': True,
                },
            )
            if created:
                self.stdout.write(f'  Service created: {title}')

    # ── Демо-пользователи ────────────────────────────────────────────────────

    def _seed_users(self):
        from core.models import User, Role

        DEMO_USERS = [
            {
                'username': 'admin',
                'email': 'admin@keypartner.ru',
                'password': 'Admin1234!',
                'first_name': 'Администратор',
                'last_name': 'Системы',
                'role_name': 'admin',
                'is_staff': True,
                'is_superuser': True,
            },
            {
                'username': 'manager',
                'email': 'manager@keypartner.ru',
                'password': 'Manager1234!',
                'first_name': 'Иван',
                'last_name': 'Петров',
                'role_name': 'manager',
                'is_staff': False,
                'is_superuser': False,
            },
            {
                'username': 'client',
                'email': 'client@keypartner.ru',
                'password': 'Client1234!',
                'first_name': 'Анна',
                'last_name': 'Смирнова',
                'role_name': 'client',
                'is_staff': False,
                'is_superuser': False,
            },
        ]

        for data in DEMO_USERS:
            if User.objects.filter(username=data['username']).exists():
                continue
            role = Role.objects.get(name=data.pop('role_name'))
            password = data.pop('password')
            user = User(**data, role=role)
            user.set_password(password)
            user.save()
            self.stdout.write(f"  User created: {user.username} / {password}")
