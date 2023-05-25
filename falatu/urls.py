from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/profiles/", include("profiles.api.v1.urls")),
    path("api-auth/", include("rest_framework.urls")),
]
