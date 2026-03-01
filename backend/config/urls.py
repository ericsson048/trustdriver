from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

from .views import frontend_app_view


urlpatterns = [
    path("admin/", admin.site.urls),
    path("docs/", include("apps.api_docs.urls")),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/", include("apps.drive.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    re_path(r"^(?!api/|admin/|docs/|media/|static/).*$", frontend_app_view, name="frontend-app"),
]
