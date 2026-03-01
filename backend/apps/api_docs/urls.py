from django.urls import path
from drf_spectacular.views import SpectacularSwaggerView

from .views import openapi_schema_view


urlpatterns = [
    path("openapi.json", openapi_schema_view, name="openapi-schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="openapi-schema"), name="swagger-ui"),
]
