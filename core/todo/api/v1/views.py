from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import TaskSerializer
from ...models import Todo
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import TasksFilter
from .paginations import CustomPagination
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly

class TaskModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = TaskSerializer
    queryset = Todo.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TasksFilter
    pagination_class = CustomPagination
    search_fields = ['title']
    ordering_fields = ['created_date']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)