from .base import *


DEBUG = True

ALLOWED_HOSTS = ['*']

CORS_ORIGIN_WHITELIST = (
	'http://localhost:8080',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': root('api_tareas/db.sqlite3'),
    }
}
