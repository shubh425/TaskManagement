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
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        password = validated_data['password']
        validated_data['password'] = make_password(password)  # Hash the password
        return super().create(validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserRegisterSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password','password_confirmation']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def save(self):
        password = self.validated_data['password']
        password_confirmation = self.validated_data['password_confirmation']

        if password != password_confirmation:
            raise serializers.ValidationError({'error': 'Passwords do not match'})
        
        if CustomUser.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'email already exists'})
        
        account = CustomUser(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(make_password(password))
        account.save()

        return account