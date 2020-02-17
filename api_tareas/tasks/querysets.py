from django.db import models


class TaskQuerySet(models.QuerySet):

	def undones(self):
		return self.filter(is_done=False)

	def dones(self):
		return self.filter(is_done=True)
