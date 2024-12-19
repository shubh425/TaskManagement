from .models import Task, CustomUser
from .serializers import TaskSerializer
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrOwner
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
import django_filters


class TaskFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name='status', lookup_expr='icontains')
    due_date = django_filters.DateFilter(field_name='due_date', lookup_expr='exact')
    
    class Meta:
        model = Task
        fields = ['status', 'due_date']


class TaskPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsAdminOrOwner]
    pagination_class = TaskPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter

    def get_queryset(self):
        """Admin sees all tasks; regular users see only their tasks."""
        user = self.request.user
        if user.role == 'admin':
            return Task.objects.filter(is_active=True)
        return Task.objects.filter(user=user, is_active=True)

    def perform_create(self, serializer):
        """Admin can create tasks for any user; regular users only for themselves."""
        user = self.request.user
        if user.role == 'admin':
            # Admin can specify the user to assign the task to
            assigned_user = self.request.data.get("user")
            if assigned_user:
                serializer.save(user_id=assigned_user)
            else:
                serializer.save(user=user)
        else:
            # Regular user can only assign tasks to themselves
            serializer.save(user=user)

    def create(self, request, *args, **kwargs):
        """Custom response for task creation."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"detail": "Task created successfully.", "task": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        """Allow regular users to update only their own tasks, and admins to reassign tasks."""
        instance = self.get_object()

        # Check if the user is authorized to update the task
        if request.user.role != 'admin' and instance.user != request.user:
            return Response(
                {"detail": "You are not authorized to update this task."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Handle partial updates (PATCH) or full updates (PUT)
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Update the task, including reassignment if allowed
        if request.user.role == 'admin':
            # Admin can update the `user` field to reassign the task
            new_user_id = request.data.get('user')
            if new_user_id:
                try:
                    new_user = CustomUser.objects.get(id=new_user_id)
                    instance.user = new_user
                except CustomUser.DoesNotExist:
                    return Response(
                        {"detail": f"User with id {new_user_id} does not exist."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

        # Save other updated fields
        self.perform_update(serializer)

        return Response(
            {"detail": "Task updated successfully.", "task": serializer.data},
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        """Admin can delete any task; regular users can delete only their tasks."""
        try:
            task = self.get_queryset().get(pk=kwargs["pk"])
        except Task.DoesNotExist:
            return Response(
                {"detail": "Task not found or it is no longer active."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check if the user is authorized to delete this task
        if request.user.role != 'admin' and task.user != request.user:
            return Response(
                {"detail": "You are not authorized to delete this task."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Perform soft delete (mark as inactive)
        task.is_active = False
        task.save()
        return Response(
            {"detail": "Task marked as inactive."},
            status=status.HTTP_204_NO_CONTENT,
        )

    def retrieve(self, request, *args, **kwargs):
        """Admin can view any task; regular users can view only their tasks."""
        try:
            task = self.get_queryset().get(pk=kwargs["pk"])
        except Task.DoesNotExist:
            return Response(
                {"detail": "Task not found or it is no longer active."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check if the user is authorized to view this task
        if request.user.role != 'admin' and task.user != request.user:
            return Response(
                {"detail": "You are not authorized to view this task."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = self.get_serializer(task)
        return Response(
            {"detail": "Task retrieved successfully.", "task": serializer.data},
            status=status.HTTP_200_OK,
        )
