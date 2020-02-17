from django.urls import path
from . import views


urlpatterns = [
	path('', views.TaskListCreateAPIView.as_view(), name='list_and_create'),
	path('<int:pk>/done', views.mark_as_done, name='mark_as_done'),
	path('<int:pk>', views.TaskRetrieveDestroyAPIView.as_view(), name='detail_and_destroy'),
]
