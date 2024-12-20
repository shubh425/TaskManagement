from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


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
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password_confirmation']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_email(self, value):
        """Check if the email is already in use."""
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate(self, data):
        """Ensure passwords match."""
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        """Create a new user with a hashed password."""
        validated_data.pop('password_confirmation')  # Remove password_confirmation
        validated_data['password'] = make_password(validated_data['password'])
        return CustomUser.objects.create(**validated_data)