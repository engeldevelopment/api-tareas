from django.urls import path, include
from .api import routers

app_name = 'tasks'

urlpatterns = [
	path('', include(routers.urlpatterns)),
]

