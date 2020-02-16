from django.urls import path
from . import views


urlpatterns = [
	path('', views.TaskListCreateAPIView.as_view(), name='list_and_create')
]
