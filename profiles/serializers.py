from rest_framework import serializers

from .models import User, Profile, Message


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
        fields = ['id', 'user', 'full_name', 'bio', 'image', 'verified']
        extra_kwargs = {
            'user': {'read_only': True}
        }
