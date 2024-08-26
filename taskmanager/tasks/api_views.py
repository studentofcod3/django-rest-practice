from rest_framework import viewsets
from tasks.models import Task, Category
from tasks.serializers import TaskSerializer, CategorySerializer
from tasks.tasks import send_task_creation_email
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        task = serializer.save()
        send_task_creation_email.delay(task.id)


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]