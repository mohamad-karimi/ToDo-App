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
    '''
    ViewSet for managing user tasks.
    Provides CRUD operations, filtering, searching, ordering,
    pagination, and permission control.
    '''
        
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TasksFilter
    pagination_class = CustomPagination
    search_fields = ['title']
    ordering_fields = ['created_date']

    def get_queryset(self):
        '''
        Return only the tasks that belong to the authenticated user.
        '''
                
        return Todo.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        '''
        Automatically assign the authenticated user as the owner
        when creating a new task.
        '''
                
        serializer.save(user=self.request.user)