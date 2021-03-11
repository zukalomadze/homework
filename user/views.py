from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.test import APIClient
from rest_framework.views import APIView

from product.models import Cart
from user.models import User
from user.serializers import UserSerializer, UserRegisterSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class RegistrationView(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)
        Cart.objects.create(owner=user)
        data = {'token': token.key}
        return Response(data=data, status=status.HTTP_200_OK)
