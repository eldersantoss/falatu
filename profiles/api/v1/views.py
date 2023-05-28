from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from ...models import Profile
from .serializers import ProfileSerializer


class ProfileCreateView(CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileDetailView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_url_kwarg = "username"
    lookup_field = "user__username"
