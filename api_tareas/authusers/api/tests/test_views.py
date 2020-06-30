from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from ..end_points import AUTHUSERS_OBTAIN_TOKEN


class AuthWithTokenAPIViewTest(APITestCase):

	def setUp(self):
		self.user = User.objects.create_user(
			username="engel",
			password='1234.1234'
		)
		self.url = AUTHUSERS_OBTAIN_TOKEN

	def test_return_a_token_gived_a_username_and_password(self):

		data = {
			'username': "engel",
			'password': "1234.1234"
		}

		response = self.client.post(self.url, data)

		self.assertIsNotNone(response.data['token'])
		self.assertEqual(status.HTTP_200_OK, response.status_code)

	def test_with_a_username_and_password_invalid_will_give_a_error(self):

		data = {
			'username': "otro.",
			'password': "otra.otro"
		}

		response = self.client.post(self.url, data)
		token = response.data.get('token', None)

		self.assertIsNone(token)
		self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
