from .models import Evaluate
from rest_framework import serializers

class EvaluateSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Evaluate
		fields = ('store', 'star')
