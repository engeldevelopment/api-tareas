from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from api_tareas.tasks.models import Task


def create_user_with_credentials(username, password):
		user = User.objects.create_user(
			username=username,
			password=password
		)
		return user


def obtain_token_for_user(username, password, client):
		url_auth_token = reverse('authusers:obtain_token')
		response = client.post(url_auth_token, {
			'username': username,
			'password': password
			}
		)
		return response.data['token']


def set_token(token, client):
	client.credentials(HTTP_AUTHORIZATION='Token ' + token)


class TaskListCreateAPIViewTest(APITestCase):

	def setUp(self):
		self.url = reverse('tasks:list_and_create')

		create_user_with_credentials(
			username='engel',
			password='engel.engel'
		)
		self.data = {}
		self.token = obtain_token_for_user(
			username='engel',
			password='engel.engel',
			client=self.client
		)
		set_token(token=self.token, client=self.client)

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

	def test_debo_pasar_un_token_valido_para_poder_crear_una_tarea(self):

		self.data['name'] = "Nueva tarea"
		set_token(token='invalid-token', client=self.client)

		response = self.client.post(self.url, self.data)

		self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

	def test_el_usuario_logueado_no_tiene_tareas_creadas(self):

		response = self.client.get(self.url)

		self.assertEqual(0, response.data['count'])

	def test_si_el_usuario_logueado_crea_una_tarea_tendra_una(self):

		self.data['name'] = "Mi tarea"

		self.client.post(self.url, self.data)

		response = self.client.get(self.url)

		self.assertEqual(1, response.data['count'])


class TaskMarkAsDoneViewSetTest(APITestCase):

	def setUp(self):

		self.user = create_user_with_credentials('engel', 'engel.engel')
		self.token = obtain_token_for_user(
			username='engel',
			password='engel.engel',
			client=self.client
		)
		set_token(token=self.token, client=self.client)

		self.task = Task.objects.create(
			name="Nueva tarea",
			owner=self.user
		)

	def test_puedo_marcar_como_terminada_una_tarea(self):

		url = reverse('tasks:mark_as_done', args=[self.task.id])

		response = self.client.patch(url)

		self.assertEqual(status.HTTP_200_OK, response.status_code)

	def test_debo_pasar_un_token_valido_para_marcar_como_terminada_una_tarea(self):

		set_token(token='invalid-token', client=self.client)

		url = reverse('tasks:mark_as_done', args=[self.task.id])

		response = self.client.patch(url)

		self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

	def test_no_puedo_marcar_una_tarea_que_no_existe_como_terminada(self):

		url = reverse('tasks:mark_as_done', args=[3])

		response = self.client.patch(url)

		self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

	def test_solo_puedo_marcar_mis_tareas_como_terminadas(self):

		user2 = create_user_with_credentials(
			username='angel',
			password='angel.angel'
		)

		task = Task.objects.create(
			name="Nueva tarea",
			owner=user2
		)

		url = reverse('tasks:mark_as_done', args=[task.id])

		response = self.client.patch(url)

		self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)


class TaskRetrieveDestroyAPIViewTest(APITestCase):

	def setUp(self):
		self.user = create_user_with_credentials(
			username='engel',
			password='engel.engel'
		)

		self.otro_usuario = create_user_with_credentials(
			username='otro',
			password='otro.otro'
		)

		self.token = obtain_token_for_user(
			username='engel',
			password='engel.engel',
			client=self.client
		)

		set_token(token=self.token, client=self.client)

		self.task = Task.objects.create(
			name="Nueva tarea",
			owner=self.user
		)

		self.task_ajena = Task.objects.create(
			name="Tarea de otro usuario",
			owner=self.otro_usuario
		)

		self.URL = 'tasks:detail_and_destroy'
		self.url = reverse(self.URL, args=[self.task.id])

	def test_solo_puedo_ver_mis_tareas(self):

		response = self.client.get(self.url)

		self.assertEqual(status.HTTP_200_OK, response.status_code)

	def test_no_puedo_ver_las_tareas_de_otros_usuarios(self):

		url = reverse(self.URL, args=[self.task_ajena.id])

		response = self.client.get(url)

		self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

	def test_debo_pasar_un_token_valido_para_ver_el_detalle_de_mi_tarea(self):

		set_token(token='invalid-token', client=self.client)

		response = self.client.get(self.url)

		self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

	def test_puedo_eliminar_mis_tareas(self):

		response = self.client.delete(self.url)

		self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

	def test_no_puedo_eliminar_las_tareas_de_otros_usuarios(self):

		url = reverse(self.URL, args=[self.task_ajena.id])

		response = self.client.delete(url)

		self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

	def test_no_puedo_eliminar_mis_tareas_si_no_estoy_logueado(self):

		set_token(token='invalid-token', client=self.client)

		response = self.client.delete(self.url)

		self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
