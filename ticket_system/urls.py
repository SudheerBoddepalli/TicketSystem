# ticket_system/urls.py (top-level)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# ticket_system/urls.py (continuation)
urlpatterns = [
    path('admin/', admin.site.urls),
    # root-level auth urls (names: 'login','logout','password_reset', etc)
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('booking.urls', namespace='booking')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
