from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User, Profile, Message, Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'name', 'surname',
                  'title', 'phone_number', 'country', 'state_region',
                  'city', 'bio', 'image', 'verified',
                  'is_builder', 'created_at', 'services', 'tasks']
        extra_kwargs = {
            'user': {'read_only': True}
        }


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'message', 'attachment']
        extra_kwargs = {
            'sender': {'read_only': True},
            'receiver': {'read_only': True}
        }


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id', 'customer', 'assignee', 'title',
            'description', 'category', 'budget',
            'start_date', 'end_date',
            'created_at', 'updated_at', 'address', 'phone_number', 'image']
        extra_kwargs = {
            'customer': {'read_only': True},
            'assignee': {'read_only': True}
        }
