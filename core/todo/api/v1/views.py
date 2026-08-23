from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import TaskSerializer
from ...models import Tasks
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import TasksFilter
from .paginations import CustomPagination
from .permissions import IsOwnerOrReadOnly
import requests
from rest_framework.response import Response
from rest_framework.views import APIView


class TaskModelViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user tasks.
    Provides CRUD operations, filtering, searching, ordering,
    pagination, and permission control.
    """

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TasksFilter
    pagination_class = CustomPagination
    search_fields = ["title"]
    ordering_fields = ["created_date"]

    def get_queryset(self):
        """
        Return only the tasks that belong to the authenticated user.
        """

        return Tasks.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically assign the authenticated user as the owner
        when creating a new task.
        """

        serializer.save(user=self.request.user)


class WeatherAPIView(APIView):
    def get(self, request):
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": 35.8400,
                "longitude": 50.9391,
                "current": (
                    "temperature_2m,"
                    "relative_humidity_2m,"
                    "weather_code,"
                    "wind_speed_10m"
                ),
                "timezone": "Asia/Tehran",
            },
            timeout=10,
        )

        response.raise_for_status()
        data = response.json()

        weather_data = {
            "temperature": data["current"]["temperature_2m"],
            "humidity": data["current"]["relative_humidity_2m"],
            "weather_code": data["current"]["weather_code"],
            "wind_speed": data["current"]["wind_speed_10m"],
        }

        return Response(weather_data)
