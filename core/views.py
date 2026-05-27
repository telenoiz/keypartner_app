"""
View-функции приложения core.
Требования: F01–F14 (1.4_Analiz_Trebovaniy_Polzovateley.md)

Реализованы как заглушки — полная логика добавляется в ВКР-033–037.
Каждый view уже содержит корректную защиту доступа.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# Роль по умолчанию для самостоятельной регистрации (F01)
ROLE_CLIENT = 'client'


# ─── Публичные страницы ──────────────────────────────────────────────────────

def home_view(request):
    """Главная страница — доступна всем (ВКР-033)."""
    return render(request, 'core/home.html')


def contacts_view(request):
    """Страница контактов с формой обратной связи (ВКР-035)."""
    return render(request, 'core/contacts.html')


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
