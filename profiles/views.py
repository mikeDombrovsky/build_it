import rest_framework.pagination
from django.shortcuts import render
from rest_framework import status, generics

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from profiles.models import User, Profile, Task
from profiles.serializers import RegisterSerializer, ProfileSerializer, TaskSerializer


class RegisterView(generics.CreateAPIView):
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


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        user = request.user
        profile = user.profile

        serializer = ProfileSerializer(profile, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.user
        profile = user.profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class ProfileListView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = rest_framework.pagination.LimitOffsetPagination

    def get(self, request):
        profiles = Profile.objects.all(is_builder=True, verified=True)
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)


class TaskView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = rest_framework.pagination.LimitOffsetPagination

    def post(self, request):
        user = request.user

        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        task = Task.objects.get(id=pk)
        serializer = TaskSerializer(task, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        user = request.user
        task = Task.objects.get(customer=user, id=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)


class TaskListView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = rest_framework.pagination.LimitOffsetPagination

    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


# TODO: add filtering to TaskListView