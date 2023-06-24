from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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


class ProfileFollowersView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """
        Follow the profile if the sender doesn't follow and unfollow otherwise
        """

        logged_in_profile = self.request.user.profile
        username = self.kwargs.get("username")
        target_profile = get_object_or_404(Profile, user__username=username)

        if logged_in_profile.is_following(target_profile):
            logged_in_profile.unfollow(target_profile)
        else:
            logged_in_profile.follow(target_profile)

        return Response(
            {
                "logged_in_following": logged_in_profile.get_following_count(),
                "target_followers": target_profile.get_followers_count(),
            }
        )
