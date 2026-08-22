from rest_framework.routers import DefaultRouter
from .views import TaskModelViewSet, WeatherAPIView
from django.urls import path
from django.views.decorators.cache import cache_page

app_name = "api-v1"

router = DefaultRouter()
router.register(r"task", TaskModelViewSet, basename="task")

urlpatterns = [
    path(
        "weather/",
        cache_page(60 * 20)(WeatherAPIView.as_view()),
        name="weather",
    ),
]
urlpatterns += router.urls
