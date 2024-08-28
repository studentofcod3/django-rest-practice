from datetime import datetime

from django.db.models import Count, F, Q, ExpressionWrapper, fields
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from tasks.models import Task, Category
from tasks.serializers import TaskListSerializer, TaskSerializer, CategorySerializer, TaskUpdateSerializer

class TaskPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class TaskViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = TaskPagination
    filter_backends = [
        DjangoFilterBackend, 
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ['completed', 'category']
    ordering_fields = ['created']
    ordering = ['-created'] # Default ordering
    search_fields = ['title', 'description', 'category__name']

    def get_queryset(self):
        # USe Q objects to construct and/or statements
        qs = Task.objects.filter(
            ~Q(created__lte=datetime.today()) | Q(completed=False)
        ).annotate(
            time_since_creation=ExpressionWrapper(
                F('created') - datetime.now(),
                output_field=fields.DurationField()
            )
        )
        return qs
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TaskListSerializer
        if self.action in ['update', 'partial_update']:
            return TaskUpdateSerializer
        return TaskSerializer
    
    @action(detail=True, methods=['post'])
    def mark_complete(self, request, pk=None):
        task = self.get_object()
        task.completed = True
        task.save()
        return Response({
            'status': 'Task marked as complete'
        })


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]