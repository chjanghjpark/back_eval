# from django.shortcuts import render
from rest_framework import viewsets
from .serializers import EvaluateSerializer
from .models import Evaluate

# Create your views here.
class EvaluateViewSet(viewsets.ModelViewSet):
	queryset = Evaluate.objects.all()
	serializer_class = EvaluateSerializer
