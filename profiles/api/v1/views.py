from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from ...models import Profile
from .serializers import ProfileSerializer


class ProfileCreateView(CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
