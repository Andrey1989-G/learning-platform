from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from materials.permissions import IsObjectOwnerOrModerator
from users.models import User
from users.serializers import UserSerializer

# Create your views here.

class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    permission_classes = [IsAuthenticated, IsObjectOwnerOrModerator]


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    permission_classes = [IsAuthenticated]

class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()

    permission_classes = [IsAuthenticated, IsObjectOwnerOrModerator]