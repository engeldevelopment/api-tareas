from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Task


class TaskTest(TestCase):

	def setUp(self):
		self.user = User.objects.create_user(
			username='engel',
			password='engel.engel'
		)

		self.task = Task.objects.create(
			name="Tarea",
			owner=self.user
		)

	def test_crear_una_tarea(self):

		with self.assertNumQueries(1):
			Task.objects.create(
				name="Tarea",
				owner=self.user
			)

	def test_se_puede_marcar_como_terminada(self):

		self.task.mark_as_done()

		self.assertTrue(self.task.is_done)
