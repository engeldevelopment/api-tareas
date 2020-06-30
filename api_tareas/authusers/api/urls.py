from django.urls import path

from rest_framework.authtoken import views as views_auth

app_name = 'authusers'

urlpatterns = [
	path('obtain-token', views_auth.obtain_auth_token, name='obtain_token'),
]
