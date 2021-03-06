from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .permissions import IsOwnerOrDeny
from .serializers import TaskSerializer
from ..models import Task


class TaskListCreateAPIView(generics.ListCreateAPIView):
	serializer_class = TaskSerializer
	authentication_classes = (TokenAuthentication, )
	permission_classes = (IsAuthenticated, )

	def get_queryset(self):
		return self.request.user.tasks.undones()

	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)


class TaskRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
	serializer_class = TaskSerializer
	queryset = Task.objects.all()
	authentication_classes = (TokenAuthentication, )
	permission_classes = (IsAuthenticated, IsOwnerOrDeny,)


class TaskMarkAsDoneViewSet(viewsets.ViewSet):
	permission_classes = (IsAuthenticated, )
	authentication_classes = (TokenAuthentication, )

	def done(self, request, pk):
		task = get_object_or_404(Task, pk=pk)

		if request.user != task.owner:
			raise PermissionDenied('No puedes marcar como terminada las tareas de otros usuarios.')

		task.mark_as_done()

		return Response(status=status.HTTP_200_OK)


mark_as_done = TaskMarkAsDoneViewSet.as_view({"patch": "done"})
