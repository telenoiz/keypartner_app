from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

# Обработчик 404 (ВКР-036). Активен при DEBUG=False.
handler404 = 'core.views.handler404_view'
