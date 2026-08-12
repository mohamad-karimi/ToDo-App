from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import TaskSerializer
from ...models import Todo
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import TasksFilter
from .paginations import CustomPagination
from .permissions import IsOwnerOrReadOnly

class TaskModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TasksFilter
    pagination_class = CustomPagination
    search_fields = ['title']
    ordering_fields = ['created_date']

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)