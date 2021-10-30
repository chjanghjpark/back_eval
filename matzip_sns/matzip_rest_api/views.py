# from django.shortcuts import render
from rest_framework import viewsets
from .serializers import EvaluateSerializer
from .models import Evaluate
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect

# Create your views here.
class EvaluateViewSet(viewsets.ModelViewSet):
	queryset = Evaluate.objects.all()
	serializer_class = EvaluateSerializer

# @csrf_protect
class KakaoLoginView(View):
	def get(self, request):
		dummy_data = {
			'name': 'jch',
			'nik': 'cjang'
		}
		return JsonResponse(dummy_data)
	def post(self, request):
		api_url = 'https://kapi.kakao.com/v2/user/me'
		kakao_token = request.header.get('access_token', None)
		token_type = 'bearer'

		if not kakao_token:
			return JsonResponse({'message': 'TOKEN_REQUIRED'}, status=400)
		else:
			return JsonResponse({'message': 'OK'}, status=200)
