from .models import Task, CustomUser
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'task_name', 'description', 'due_date', 'status', 'user']
        read_only_fields = ['user']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser  # Use CustomUser if you have a custom user model
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        password = validated_data['password']
        validated_data['password'] = make_password(password)  # Hash the password
        return super().create(validated_data)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
