from rest_framework import serializers

from ..models import Task


class TaskSerializer(serializers.ModelSerializer):
	class Meta:
		model = Task
		fields = ('id', 'name', 'is_done')

	def validate_name(self, name):

		if name.isdigit():
			raise serializers.ValidationError('El nombre no puede ser numérico')
		return name
