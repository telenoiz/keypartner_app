from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

# Медиафайлы в режиме разработки (ВКР-045)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Обработчик 404 (ВКР-036). Активен при DEBUG=False.
handler404 = 'core.views.handler404_view'
