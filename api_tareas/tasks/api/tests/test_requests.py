from django.test import SimpleTestCase
from django.urls import resolve
from .. import views


class TaskRequestTest(SimpleTestCase):

	def test_post_and_get_tasks(self):

		url = '/api/v1/tasks/'

		self.assertEqual(views.TaskListCreateAPIView, resolve(url).func.view_class)
