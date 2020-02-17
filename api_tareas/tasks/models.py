from django.contrib.auth.models import User
from django.db import models

from .managers import TaskManager


class Task(models.Model):
	name = models.CharField(max_length=30)
	is_done = models.BooleanField(default=False)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
	objects = TaskManager()

	def __str__(self):
		return self.name

	def mark_as_done(self):
		self.is_done = True
		self.save()
