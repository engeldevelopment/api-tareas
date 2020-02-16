from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase


class TaskListCreateAPIViewTest(APITestCase):

	def setUp(self):
		self.url = reverse('tasks:list_and_create')

		User.objects.create_user(
			username='engel',
			password='engel.engel'
		)
		self.data = {}

		self.client.login(
			username='engel',
			password='engel.engel'
		)

	def test_puedo_crear_una_tarea(self):

		self.data['name'] = "Nueva tarea"

		response = self.client.post(self.url, self.data)

		self.assertEqual(status.HTTP_201_CREATED, response.status_code)

	def test_da_error_si_el_nombre_esta_vacio(self):

		self.data['name'] = ""

		response = self.client.post(self.url, self.data)

		self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

	def test_el_nombre_no_puede_ser_numerico(self):

		self.data['name'] = "90030"

		response = self.client.post(self.url, self.data)

		self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

	def test_el_nombre_puede_ser_alfanumerico(self):

		self.data['name'] = "Mia 99003"

		response = self.client.post(self.url, self.data)

		self.assertEqual(status.HTTP_201_CREATED, response.status_code)

	def test_debo_estar_logueado_para_poder_crear_una_tarea(self):

		self.client.logout()

		self.data['name'] = "Nueva tarea"

		response = self.client.post(self.url, self.data)

		self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
