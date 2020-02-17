from django.db import models
from .querysets import TaskQuerySet


class TaskManager(models.Manager):

	def get_queryset(self):
		return TaskQuerySet(model=self.model, using=self._db)

	def undones(self):
		return self.get_queryset().undones()

	def dones(self):
		return self.get_queryset().dones()
