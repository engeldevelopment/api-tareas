from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/tasks/', include('api_tareas.tasks.urls')),
    path('admin-api/', include('rest_framework.urls'))
]
