from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.user.models import User

from .serielizers import UserSerializer


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )
