"""
URL-маршруты приложения core.
Требования: F01 (регистрация), F02–F05 (клиент), F06–F10 (менеджер), F11–F14 (администратор).
Настройки: LOGIN_URL='/login/', LOGIN_REDIRECT_URL='/', LOGOUT_REDIRECT_URL='/login/'
"""

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Публичные страницы
    path('',           views.home_view,      name='home'),
    path('services/',  views.services_view,  name='services'),
    path('news/',      views.news_view,      name='news'),
    path('projects/',  views.projects_view,  name='projects'),
    path('contacts/',  views.contacts_view,  name='contacts'),

    # Аутентификация (F01)
    path('login/',     views.login_view,     name='login'),
    path('register/',  views.register_view,  name='register'),
    path('logout/',    views.logout_view,    name='logout'),

    # Личный кабинет — требует авторизации (F02–F10)
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
