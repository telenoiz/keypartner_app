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
    path('dashboard/',             views.dashboard_view,      name='dashboard'),
    path('dashboard/tickets/new/',        views.ticket_create_view,  name='ticket_create'),
    path('dashboard/tickets/<int:pk>/',           views.ticket_detail_view,         name='ticket_detail'),
    path('dashboard/profile/',                    views.profile_view,               name='profile'),
    path('dashboard/notifications/',              views.notifications_view,          name='notifications'),
    path('dashboard/notifications/<int:pk>/read/', views.notification_mark_read_view, name='notification_read'),

    # ЛК Менеджера (ВКР-043/044)
    path('dashboard/manager/',                       views.manager_dashboard_view,      name='manager_dashboard'),
    path('dashboard/manager/tickets/<int:pk>/',      views.manager_ticket_detail_view,  name='manager_ticket_detail'),
    path('dashboard/manager/stats/',                 views.manager_stats_view,          name='manager_stats'),

    # Файловая система (ВКР-045)
    path('dashboard/tickets/<int:pk>/upload/',       views.attachment_upload_view,      name='attachment_upload'),
    path('attachments/<int:pk>/download/',           views.attachment_download_view,    name='attachment_download'),

    # Статические публичные страницы (ВКР-037)
    path('about/',   views.about_view,   name='about'),
    path('sitemap/', views.sitemap_view, name='sitemap'),

    # Детальная новость (ВКР-037)
    path('news/<int:pk>/', views.news_detail_view, name='news_detail'),
]
