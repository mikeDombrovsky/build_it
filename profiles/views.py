from django.shortcuts import render
from rest_framework import status, generics

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from profiles.models import User
from profiles.serializers import RegisterSerializer


class HomeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Welcome to the home page'}

        return Response(content)


class RegisterView(generics.CreateAPIView):
    # def post(self, request):
    #     try:
    #         if request.data["username"]:
    #                 username=request.data["username"]
    #
    #         user = User.objects.create(
    #             username=username,
    #             email=request.data["email"],
    #         )
    #         user.set_password(request.data["password"])
    #         user.save()
    #         return Response(status=status.HTTP_201_CREATED)
    #     except Exception as e:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)