from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.main.utils import change_language


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('user/', include('users.urls', namespace='user')),
    path('bot/', include('bot.urls', namespace='bot')),
    path('change-language/', change_language, name='change_language'),
]


handler404 = "config.middleware.errorhandler.error_404"
handler500 = "config.middleware.errorhandler.error_500"
handler403 = "config.middleware.errorhandler.error_403"
handler400 = "config.middleware.errorhandler.error_400"

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
