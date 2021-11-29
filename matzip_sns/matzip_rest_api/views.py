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
from rest_framework.views import APIView
from .about_jwt import create_token, validate_token


# Create your views here.
class UserinfoViewSet(viewsets.ModelViewSet):
	queryset = Userinfo.objects.all()
	serializer_class = UserinfoSerializer

class EvaluateViewSet(viewsets.ModelViewSet):
	queryset = Evaluate.objects.all()
	serializer_class = EvaluateSerializer

def login_api(login_site, url, token, token_type):
	if not token:
		return (JsonResponse({'message': 'TOKEN_REQUIRED'}, status=400))
	headers = {
		'Authorization': token_type + ' ' + token
	}
	response = requests.post(url, headers=headers)
	user_info = response.json()

	if login_site == "kakao":
		if not user_info.get('id'):
			return JsonResponse({'message': 'TOKEN_NOT_VALID'}, status=405)
		if not user_info.get('properties'):
			return JsonResponse({'message': 'TOKEN_NOT_VALID'}, status=405)
		if not user_info.get('properties').get('nickname'):
			return JsonResponse({'message': 'TOKEN_NOT_VALID'}, status=405)
		user_id = login_site + '_' + str(user_info.get('id'))
		user_nickname = user_info.get('properties').get('nickname')
	elif login_site == "naver":
		if not user_info.get('response'):
			return JsonResponse({'message': 'TOKEN_NOT_VALID'}, status=405)
		if not user_info.get('response').get('id'):
			return JsonResponse({'message': 'TOKEN_NOT_VALID'}, status=405)
		if not user_info.get('response').get('name'):
			return JsonResponse({'message': 'TOKEN_NOT_VALID'}, status=405)
		user_id = login_site + '_' + str(user_info.get('response').get('id'))
		user_nickname = user_info.get('response').get('name')

	user, user_flag = User.objects.get_or_create(username=user_id, password=user_id, last_name=user_nickname)
	userinfo = Userinfo.objects.get_or_create(user=user, signup_site=login_site, name=user_nickname)
	encoded_jwt = create_token(user_id, user_nickname)

	return JsonResponse({'jwt': encoded_jwt}, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class NaverLoginView(APIView):
	def post(self, request):
		login_site = "naver"
		naver_url = "https://openapi.naver.com/v1/nid/me"
		naver_token = request.headers.get('Authorization', None)
		token_type = 'Bearer'

		return login_api(login_site, naver_url, naver_token, token_type)

@method_decorator(csrf_exempt, name='dispatch')
class KakaoLoginView(APIView):
	def post(self, request):
		login_site = "kakao"
		kakao_url = "https://kapi.kakao.com/v2/user/me"
		kakao_token = request.headers.get('Authorization', None)
		token_type = 'Bearer'

		return login_api(login_site, kakao_url, kakao_token, token_type)

@method_decorator(csrf_exempt, name='dispatch')
class EvaluateView(APIView):
	def post(self, request):
		encoded_jwt = request.headers.get('Authorization', None)
		decoded_jwt = validate_token(encoded_jwt)
		user_id = decoded_jwt['user_id']
		user_nickname = decoded_jwt['nickname']
		eval_store = request.headers.get('store', None)
		eval_star = request.headers.get('star', None)

		eval_user = User.objects.get(username=user_id, password=user_id, last_name=user_nickname)
		eval = Evaluate.objects.create(store=eval_store, star=eval_star, user=eval_user)

		return JsonResponse({'message': 'success'}, status=200)
