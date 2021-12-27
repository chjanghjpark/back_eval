# from django.shortcuts import render
from rest_framework import viewsets
from matzip_rest_api.forms.serializers import EvaluateSerializer, UserinfoSerializer
from matzip_rest_api.models.models import Evaluate, Userinfo


# Create your views here.
class UserinfoViewSet(viewsets.ModelViewSet):
	queryset = Userinfo.objects.all()
	serializer_class = UserinfoSerializer
