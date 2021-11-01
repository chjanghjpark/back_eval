from .models import Evaluate, Userinfo
from rest_framework import serializers

class EvaluateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Evaluate
		fields = ("store", "star", "user")

class UserinfoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Userinfo
		fields = ("id", "name")
