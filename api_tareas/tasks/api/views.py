from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import TaskSerializer
from ..models import Task


class TaskListCreateAPIView(generics.ListCreateAPIView):
	serializer_class = TaskSerializer
	queryset = Task.objects.all()
	permission_classes = (IsAuthenticated, )

	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)
