from .models import Task
from .serializers import TaskSerializer
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrOwner
# from rest_framework_simplejwt.authentication import JWTAuthentication


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsAdminOrOwner]
    
    def get_queryset(self):
        user=self.request.user
        if user.role == 'admin':
            return Task.objects.filter(is_active=True)
        return Task.objects.filter(user=user, is_active=True)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def perform_destroy(self, request, *args, **kwargs):
        task = self.get_object()
        task.soft_delete()  # Soft delete instead of hard delete
        return Response({"detail": "Task marked as inactive."}, status=status.HTTP_204_NO_CONTENT)