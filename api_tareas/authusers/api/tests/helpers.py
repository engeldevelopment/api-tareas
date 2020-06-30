from django.contrib.auth.models import User

from ..end_points import AUTHUSERS_OBTAIN_TOKEN


def create_user_with_credentials(username, password):
	user = User.objects.create_user(
		username=username,
		password=password
	)
	return user


def obtain_token_for_user(username, password, client):
	response = client.post(AUTHUSERS_OBTAIN_TOKEN, {
		'username': username,
		'password': password
		}
	)
	return response.data['token']


def set_token(token, client):
	client.credentials(HTTP_AUTHORIZATION='Token ' + token)
