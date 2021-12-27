import requests
import json
import datetime
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from django.contrib.auth.models import User
from matzip_rest_api.models.models import Evaluate, Userinfo
from matzip_rest_api.jwt_func import create_access_token, create_refresh_token
from matzip_rest_api.jwt_func import validate_token


class LoginView(APIView):
	def post(self, request):
		token = request.headers.get('Authorization', None)
		if not token:
			return (JsonResponse({'message': 'TOKEN_REQUIRED'}, status=400))
		# print(token)
		body = json.loads(request.body.decode('utf-8'))
		print(body)
		try:
			login_site = body['login_site']
		except:
			return (JsonResponse({'message': 'login_site REQUITED'}, status=400))

		if login_site == "google":
			user_id, user_nickname = google_api(token)
		elif login_site == "kakao":
			user_id, user_nickname = kakao_api(token)
		elif login_site == "naver":
			user_id, user_nickname = naver_api(token)
		else:
			return (JsonResponse({'message': 'login_site_invalid'}, status=400))
		if user_id is None or user_nickname is None:
			return JsonResponse({'message': 'TOKEN_NOT_VALID'}, status=401)
		user, user_flag = User.objects.get_or_create(username=user_id, password=user_id, last_name=user_nickname)
		userinfo = Userinfo.objects.get_or_create(user=user, login_site=login_site)
		access_token = create_access_token(user_id, user_nickname)
		refresh_token = create_refresh_token(user_id, user_nickname)

		return JsonResponse({'access_token': access_token, 'refresh_token': refresh_token}, status=200)
	
	def get(self, request):
		refresh_token = request.headers.get('Authorization', None)
		if not refresh_token:
			return (JsonResponse({'message': 'TOKEN_REQUIRED'}, status=400))
		decoded_jwt = validate_token(refresh_token)
		user_id = decoded_jwt['user_id']
		user_nickname = decoded_jwt['nickname']
		token_exp = decoded_jwt['exp']
		# 토큰 시간 비교하기

def google_api(token):
	try:
		login_site = 'google'
		CLIENT_ID = "506826022275-kaqkf69c5ud0kt3g98s50d8sbi7stg2f.apps.googleusercontent.com"
		idinfo = id_token.verify_oauth2_token(token, Request(), CLIENT_ID)

		user_id = login_site + '_' + str(idinfo.get('sub'))
		user_nickname = idinfo.get('name')

		return (user_id, user_nickname)
	except ValueError:
		pass

def naver_api(token):
	try:
		login_site = "naver"
		url = "https://openapi.naver.com/v1/nid/me"
		token_type = 'Bearer'

		headers = {
			'Authorization': token_type + ' ' + token
		}
		response = requests.post(url, headers=headers)
		user_info = response.json()
		if not user_info.get('response'):
			return JsonResponse({'message': 'TOKEN_NOT_VALID'}, status=405)
		if not user_info.get('response').get('id'):
			return JsonResponse({'message': 'TOKEN_NOT_VALID'}, status=405)
		if not user_info.get('response').get('name'):
			return JsonResponse({'message': 'TOKEN_NOT_VALID'}, status=405)
		user_id = login_site + '_' + str(user_info.get('response').get('id'))
		user_nickname = user_info.get('response').get('name')

		return (user_id, user_nickname)
	except ValueError:
		pass

def kakao_api(token):
	try:
		login_site = "kakao"
		url = "https://kapi.kakao.com/v2/user/me"
		token_type = 'Bearer'

		headers = {
			'Authorization': token_type + ' ' + token
		}
		response = requests.post(url, headers=headers)
		user_info = response.json()
		
		user_id = login_site + '_' + str(user_info.get('id'))
		user_nickname = user_info.get('properties').get('nickname')
		return (user_id, user_nickname)
	except:
		return (None, None)
