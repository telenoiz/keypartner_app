"""
Контекстные процессоры приложения core.
Добавляют общие переменные во все шаблоны.
"""

from django.conf import settings


def site_meta(request):
    """
    Передаёт метаданные сайта во все шаблоны.
    SITE_AUTHOR — ФИО автора ВКР (требование ТЗ §9).
    """
    return {
        'SITE_AUTHOR': getattr(settings, 'SITE_AUTHOR', ''),
    }
