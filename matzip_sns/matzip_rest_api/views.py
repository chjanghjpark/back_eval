# from django.shortcuts import render
import requests
from rest_framework import viewsets
from .serializers import EvaluateSerializer, UserinfoSerializer
from .models import Evaluate, Userinfo
from django.contrib.auth.models import User
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

# Create your views here.
class UserinfoViewSet(viewsets.ModelViewSet):
	queryset = Userinfo.objects.all()
	serializer_class = UserinfoSerializer

class EvaluateViewSet(viewsets.ModelViewSet):
	queryset = Evaluate.objects.all()
	serializer_class = EvaluateSerializer



@method_decorator(csrf_exempt, name='dispatch')
class KakaoLoginView(APIView):
	def post(self, request):
		kakao_url = "https://kapi.kakao.com/v2/user/me"
		kakao_token = request.headers.get('Authorization', None)
		token_type = 'Bearer'

		if not kakao_token:
			return JsonResponse({'message': 'TOKEN_REQUIRED'}, status=400)

		headers = {
			'Authorization': token_type + ' ' + kakao_token
		}
		response = requests.post(kakao_url, headers=headers)

		user_info = response.json()
		if not user_info.get('id'):
			return JsonResponse({'message': 'TOKEN_NOT_VALID'}, status=405)

		user_id = user_info.get('id')
		user_nickname = user_info.get('properties').get('nickname')

		user, user_flag = User.objects.get_or_create(username=user_id, password=user_id, last_name=user_nickname)
		userinfo = Userinfo.objects.get_or_create(user=user, id=user_id, name=user_nickname)
		access_token, token_flag = Token.objects.get_or_create(user=user)
		return JsonResponse({'access_token': access_token.key}, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class EvaluateView(APIView):
	def post(self, request):
		user = request.user

		eval_store = request.headers.get('store', None)
		eval_star = request.headers.get('star', None)
		eval_user = User.objects.get(username=user.username, password=user.password, last_name=user.last_name)

		eval = Evaluate.objects.create(store=eval_store, star=eval_star, user=eval_user)

		return JsonResponse({'access_token': 'user'}, status=200)
