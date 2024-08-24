from rest_framework import viewsets
from tasks.models import Task, Category
from tasks.serializers import TaskSerializer, CategorySerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]