from matzip_rest_api.models.models import Evaluate, Userinfo
from rest_framework import serializers

class EvaluateSerializer(serializers.ModelSerializer):
	user = serializers.ReadOnlyField(source='user.last_name')
	class Meta:
		model = Evaluate
		fields = ("user", "store", "star")

class UserinfoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Userinfo
		fields = ("id", "user")
