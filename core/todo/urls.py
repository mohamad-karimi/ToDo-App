from django.urls import path
from . import views

app_name = "todo"

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create/', views.TodoCreateView.as_view(), name='create_task'),
    path('edit/<int:pk>/', views.TodoEditView.as_view(), name='update_task'),
    path('delete/<int:pk>/', views.TodoDeleteView.as_view(), name='delete_task'),
    path('completed/<int:pk>/', views.TodoComplete.as_view(), name='complete_task'),
    path('not-completed/<int:pk>/', views.TodoNotComplete.as_view(), name='not_complete_task'),
]