from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    return Response({"message": "API is running :)"}, status=status.HTTP_200_OK)


urlpatterns = [
    path("", health_check, name="health_check"),
    path("admin/", admin.site.urls),
    path("api/v1/profiles/", include("profiles.urls")),
    path("api/v1/posts/", include("posts.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
