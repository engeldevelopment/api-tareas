from django.contrib import admin
from django.urls import path, include

from rest_framework_swagger.views import get_swagger_view


docs_api = get_swagger_view(title="API Doc")

urlpatterns_api_v1 = [
    path('tasks/', include('api_tareas.tasks.urls')),
    path('authusers/', include('api_tareas.authusers.api.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/docs/', docs_api),
    path('api/v1/', include(urlpatterns_api_v1)),
    path('admin-api/', include('rest_framework.urls'))
]
