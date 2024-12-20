from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserCreateSerializer, UserRegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Ensure only authenticated users can register
def create_user(request):
    if request.user.role != 'admin':  # Check if the current user is an admin
        return Response({"detail": "You are not authorized to create users."}, status=status.HTTP_403_FORBIDDEN)

    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"detail": "User created successfully.", "user": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def registration_view(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        account = serializer.save()
        data = {
            "username": account.username,
            "email": account.email,
            "token": {
                "refresh": str(RefreshToken.for_user(account)),
                "access": str(RefreshToken.for_user(account).access_token),
            },
        }
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)