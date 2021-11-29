# from django.shortcuts import render
import requests
from rest_framework import viewsets
from matzip_rest_api.forms.serializers import EvaluateSerializer, UserinfoSerializer
from matzip_rest_api.models.models import Evaluate, Userinfo
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from matzip_rest_api.jwt_func import create_access_token
from google.oauth2 import id_token
from google.auth.transport.requests import Request


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
	# print(user_info)
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
	encoded_jwt = create_access_token(user_id, user_nickname)

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
class GoogleLoginView(APIView):
	# (Receive token by HTTPS POST)
	# ...
	def post(self, request):
		try:
			# Specify the CLIENT_ID of the app that accesses the backend:
			google_token = request.headers.get('Authorization', None)
			# google_validate_id_token(google_token)
			CLIENT_ID = "506826022275-kaqkf69c5ud0kt3g98s50d8sbi7stg2f.apps.googleusercontent.com"
			idinfo = id_token.verify_oauth2_token(google_token, Request(), CLIENT_ID)
			# print(idinfo)
			# Or, if multiple clients access the backend server:
			# idinfo = id_token.verify_oauth2_token(token, requests.Request())
			# if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
			#     raise ValueError('Could not verify audience.')

			# If auth request is from a G Suite domain:
			# if idinfo['hd'] != GSUITE_DOMAIN_NAME:
			#     raise ValueError('Wrong hosted domain.')

			# ID token is valid. Get the user's Google Account ID from the decoded token.
			# userid = idinfo['sub']
			login_site = 'google'
			user_id = login_site + '_' + str(idinfo.get('sub'))
			# print(user_id)
			user_nickname = idinfo.get('name')

			user, user_flag = User.objects.get_or_create(username=user_id, password=user_id, last_name=user_nickname)
			userinfo = Userinfo.objects.get_or_create(user=user, signup_site=login_site, name=user_nickname)
			encoded_jwt = create_access_token(user_id, user_nickname)

			return JsonResponse({'jwt': encoded_jwt}, status=200)
			
		except ValueError:
			# Invalid token
			pass

