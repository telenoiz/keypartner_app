"""
View-функции приложения core.
Требования: F01–F14 (1.4_Analiz_Trebovaniy_Polzovateley.md)
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as auth_logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.urls import reverse

from django.core.paginator import Paginator

from .models import Service, News, Project, Role, Notification
from .forms import ContactMessageForm, LoginForm, RegisterForm, ProjectCreateForm, ProfileUpdateForm

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

# Сообщения аутентификации (ВКР-036)
REGISTER_SUCCESS_MESSAGE = 'Добро пожаловать! Аккаунт успешно создан.'
REGISTER_ROLE_NOT_FOUND  = (
    'Не удалось назначить роль. Обратитесь к администратору.'
)

# Лимиты страниц контента (ВКР-034)
SERVICES_PER_PAGE  = 20
NEWS_PER_PAGE      = 10
PROJECTS_PER_PAGE  = 9   # кратно 3 — сетка 3-в-ряд

# Дашборд клиента (ВКР-038)
DASHBOARD_TICKETS_PER_PAGE = 10
TICKET_CREATE_SUCCESS_MESSAGE = 'Заявка успешно создана. Мы свяжемся с вами в ближайшее время.'

# Детальная заявка (ВКР-040)
TICKET_NOT_FOUND_MESSAGE = 'Заявка не найдена или недоступна.'

# Профиль и уведомления (ВКР-041)
PROFILE_UPDATE_SUCCESS  = 'Профиль успешно обновлён.'
NOTIFICATIONS_PER_PAGE  = 20


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


# ─── Статические публичные страницы (ВКР-037) ───────────────────────────────

def about_view(request):
    """
    О компании — статическая публичная страница.
    Доступна всем. Закрывает критерий §4 «≥10 страниц».
    """
    return render(request, 'core/about.html')


def sitemap_view(request):
    """
    Карта сайта — структурированный список всех разделов.
    Доступна всем. Закрывает критерий §4 «≥10 страниц».
    """
    return render(request, 'core/sitemap.html')


def news_detail_view(request, pk):
    """
    Детальная страница новости.
    Доступна всем. 404 если новость не опубликована (published_at is None).
    """
    news_item = get_object_or_404(
        News.objects.select_related('author'),
        pk=pk,
        published_at__isnull=False,
    )
    return render(request, 'core/news_detail.html', {'news_item': news_item})


# ─── Аутентификация (F01) ────────────────────────────────────────────────────

def login_view(request):
    """
    Форма входа (F01). Только для анонимных пользователей.
    POST: authenticate() → login() → redirect to ?next= или LOGIN_REDIRECT_URL.
    """
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'core:home'
            return redirect(next_url)
    else:
        form = LoginForm(request)

    return render(request, 'core/login.html', {
        'form': form,
        'next': request.GET.get('next', ''),
    })


def register_view(request):
    """
    Форма регистрации (F01). Только для анонимных пользователей.
    Назначает роль ROLE_CLIENT, хэширует пароль, автоматически выполняет вход.
    """
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                role_client = Role.objects.get(name=ROLE_CLIENT)
            except Role.DoesNotExist:
                messages.error(request, REGISTER_ROLE_NOT_FOUND)
                return render(request, 'core/register.html', {'form': form})

            user = form.save(commit=False)
            user.role = role_client
            user.save()
            auth_login(request, user)
            messages.success(request, REGISTER_SUCCESS_MESSAGE)
            return redirect('core:home')
    else:
        form = RegisterForm()

    return render(request, 'core/register.html', {'form': form})


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
    Дашборд клиента — список его заявок с пагинацией и счётчиками по статусам (F03).
    Требует авторизации. Неавторизованных редиректит на /login/?next=/dashboard/.
    Полная реализация: ВКР-038.
    """
    tickets_qs = (
        Project.objects
        .filter(user=request.user)
        .select_related('service', 'priority')
        .order_by('-created_at')
    )

    # Счётчики по статусам для stat-cards
    stats = {
        'new':         tickets_qs.filter(status=Project.STATUS_NEW).count(),
        'in_progress': tickets_qs.filter(status=Project.STATUS_IN_PROGRESS).count(),
        'resolved':    tickets_qs.filter(
                           status__in=[Project.STATUS_RESOLVED, Project.STATUS_CLOSED]
                       ).count(),
        'total':       tickets_qs.count(),
    }

    paginator = Paginator(tickets_qs, DASHBOARD_TICKETS_PER_PAGE)
    page_obj  = paginator.get_page(request.GET.get('page'))

    return render(request, 'core/dashboard.html', {
        'page_obj': page_obj,
        'stats':    stats,
    })


@login_required
def ticket_create_view(request):
    """
    Форма создания новой заявки клиентом (F02).
    POST: сохраняет заявку со статусом STATUS_NEW и текущим пользователем.
    Redirect-after-POST → дашборд.
    """
    if request.method == 'POST':
        form = ProjectCreateForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user   = request.user
            ticket.status = Project.STATUS_NEW
            ticket.save()
            messages.success(request, TICKET_CREATE_SUCCESS_MESSAGE)
            return redirect(reverse('core:dashboard'))
        return render(request, 'core/ticket_create.html', {'form': form})

    form = ProjectCreateForm()
    return render(request, 'core/ticket_create.html', {'form': form})


# ─── Детальная заявка клиента (ВКР-040) ─────────────────────────────────────

@login_required
def ticket_detail_view(request, pk):
    """
    Детальная страница заявки клиента (F03, F05).
    Клиент видит только свои заявки — фильтр по user=request.user.
    Показывает: статус, описание, комментарии, список вложений (имена).
    """
    ticket = get_object_or_404(
        Project.objects
        .select_related('service', 'priority', 'manager')
        .prefetch_related('comments__user', 'attachments'),
        pk=pk,
        user=request.user,
    )
    return render(request, 'core/ticket_detail.html', {'ticket': ticket})


# ─── Профиль и уведомления (ВКР-041) ────────────────────────────────────────

@login_required
def profile_view(request):
    """
    Профиль пользователя — просмотр и редактирование (F01).
    GET: отображает форму с текущими данными.
    POST: сохраняет first_name, last_name, email.
    """
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, PROFILE_UPDATE_SUCCESS)
            return redirect(reverse('core:profile'))
        return render(request, 'core/profile.html', {'form': form})

    form = ProfileUpdateForm(instance=request.user)
    return render(request, 'core/profile.html', {'form': form})


@login_required
def notifications_view(request):
    """
    Список уведомлений пользователя с пагинацией (F04).
    Показывает непрочитанные первыми.
    """
    notifications_qs = (
        Notification.objects
        .filter(user=request.user)
        .select_related('project')
        .order_by('is_read', '-created_at')
    )
    unread_count = notifications_qs.filter(is_read=False).count()

    paginator = Paginator(notifications_qs, NOTIFICATIONS_PER_PAGE)
    page_obj  = paginator.get_page(request.GET.get('page'))

    return render(request, 'core/notifications.html', {
        'page_obj':     page_obj,
        'unread_count': unread_count,
    })


@login_required
@require_POST
def notification_mark_read_view(request, pk):
    """
    Отметить уведомление прочитанным (POST).
    Проверяет владельца — чужое уведомление → 404.
    """
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save(update_fields=['is_read'])
    return redirect(reverse('core:notifications'))


# ─── Обработчики ошибок (ВКР-036) ───────────────────────────────────────────

def handler404_view(request, exception=None):
    """
    Страница 404 — ресурс не найден.
    Регистрируется в keypartner/urls.py как handler404.
    Работает только при DEBUG=False.
    """
    return render(request, '404.html', status=404)
