"""
View-функции приложения core.
Требования: F01–F14 (1.4_Analiz_Trebovaniy_Polzovateley.md)
"""

from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.urls import reverse

from .models import Service, News, Project
from .forms import ContactMessageForm

# ─── Константы ──────────────────────────────────────────────────────────────

# Роль по умолчанию для самостоятельной регистрации (F01)
ROLE_CLIENT = 'client'

# Количество записей на главной странице (ВКР-033)
HOME_SERVICES_COUNT = 3
HOME_NEWS_COUNT     = 3

# Сообщение об успешной отправке обращения (ВКР-035)
CONTACT_SUCCESS_MESSAGE = (
    'Ваше обращение принято. Мы свяжемся с вами в ближайшее время.'
)

# Лимиты страниц контента (ВКР-034)
SERVICES_PER_PAGE  = 20
NEWS_PER_PAGE      = 10
PROJECTS_PER_PAGE  = 9   # кратно 3 — сетка 3-в-ряд


# ─── Публичные страницы ──────────────────────────────────────────────────────

def home_view(request):
    """
    Главная страница — доступна всем.
    Передаёт активные услуги и последние новости (ВКР-033).
    Требования: F02 (точка входа для подачи заявки через контакты).
    """
    services = (
        Service.objects
        .filter(is_active=True)
        .order_by('title')[:HOME_SERVICES_COUNT]
    )
    news = (
        News.objects
        .filter(published_at__isnull=False)
        .order_by('-published_at')
        .select_related('author')[:HOME_NEWS_COUNT]
    )
    return render(request, 'core/home.html', {
        'services': services,
        'news':     news,
    })


def services_view(request):
    """
    Каталог услуг — полный список активных услуг, сгруппированных по категории.
    Доступна всем. Требования: F02 (точка входа к услугам перед подачей заявки).
    """
    services = (
        Service.objects
        .filter(is_active=True)
        .select_related('category')
        .order_by('category__name', 'title')[:SERVICES_PER_PAGE]
    )
    return render(request, 'core/services.html', {'services': services})


def news_view(request):
    """
    Лента новостей компании — только опубликованные записи.
    Доступна всем.
    """
    news_items = (
        News.objects
        .filter(published_at__isnull=False)
        .select_related('author')
        .order_by('-published_at')[:NEWS_PER_PAGE]
    )
    return render(request, 'core/news.html', {'news_items': news_items})


def projects_view(request):
    """
    Публичное портфолио — завершённые и закрытые заявки.
    Личные данные клиента не раскрываются (ВКР-034).
    """
    projects = (
        Project.objects
        .filter(status__in=Project.PORTFOLIO_STATUSES)
        .select_related('service', 'service__category')
        .order_by('-created_at')[:PROJECTS_PER_PAGE]
    )
    return render(request, 'core/projects.html', {'projects': projects})


def contacts_view(request):
    """
    Страница контактов с формой обратной связи (ВКР-035).
    GET  — отображает форму (поля name/email предзаполнены для авторизованных).
    POST — сохраняет ContactMessage, redirect-after-POST → success banner.
    Доступна всем ролям и анонимным пользователям (F02).
    """
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            if request.user.is_authenticated:
                contact.user = request.user
            contact.save()
            messages.success(request, CONTACT_SUCCESS_MESSAGE)
            return redirect(reverse('core:contacts'))
        # Невалидная форма — повторный рендер с ошибками (без редиректа)
        return render(request, 'core/contacts.html', {'form': form})

    # GET — предзаполнение для авторизованных пользователей
    initial = {}
    if request.user.is_authenticated:
        first = request.user.first_name.strip()
        last  = request.user.last_name.strip()
        initial['name']  = f'{first} {last}'.strip() or request.user.username
        initial['email'] = request.user.email

    form = ContactMessageForm(initial=initial)
    return render(request, 'core/contacts.html', {'form': form})


# ─── Аутентификация (F01) ────────────────────────────────────────────────────

def login_view(request):
    """
    Форма входа — только для анонимных пользователей.
    Авторизованных редиректит на главную.
    Полная реализация (форма, валидация) — ВКР-036.
    """
    if request.user.is_authenticated:
        return redirect('core:home')
    return render(request, 'core/login.html')


def register_view(request):
    """
    Форма регистрации — только для анонимных пользователей.
    При регистрации присваивается роль ROLE_CLIENT.
    Полная реализация — ВКР-036.
    """
    if request.user.is_authenticated:
        return redirect('core:home')
    return render(request, 'core/register.html')


@require_POST
def logout_view(request):
    """
    Выход из системы — только POST (защита от CSRF-logout через GET).
    Редирект на LOGIN_URL определён в settings.LOGOUT_REDIRECT_URL.
    """
    auth_logout(request)
    return redirect('core:login')


# ─── Личный кабинет (F02–F10) ───────────────────────────────────────────────

@login_required
def dashboard_view(request):
    """
    Дашборд — требует авторизации.
    Неавторизованных редиректит на /login/?next=/dashboard/
    Полная реализация (роль-зависимые представления) — ВКР-037.
    """
    return render(request, 'core/dashboard.html')
