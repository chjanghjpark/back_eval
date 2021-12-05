import requests
import json
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from django.contrib.auth.models import User
from matzip_rest_api.models.models import Evaluate, Userinfo
from matzip_rest_api.jwt_func import create_access_token, create_refresh_token

kakao_url = "https://kapi.kakao.com/v2/user/me"
token_type = 'Bearer'

class LoginView(APIView):
	def post(self, request):
		token = request.headers.get('Authorization', None)
		# print(token)
		body = json.loads(request.body.decode('utf-8'))
		login_site = body['login_site']

		if not token:
			return (JsonResponse({'message': 'TOKEN_REQUIRED'}, status=400))

		if login_site == "google":
			user_id, user_nickname = google_api(token)
		elif login_site == "kakao":
			user_id, user_nickname = kakao_api(token)
		elif login_site == "naver":
			user_id, user_nickname = naver_api(token)
		else:
			return (JsonResponse({'message': 'login_site_invalid'}, status=400))

		user, user_flag = User.objects.get_or_create(username=user_id, password=user_id, last_name=user_nickname)
		userinfo = Userinfo.objects.get_or_create(user=user, signup_site=login_site, name=user_nickname)
		access_token = create_access_token(user_id, user_nickname)
		refresh_token = create_refresh_token(user_id, user_nickname)

		return JsonResponse({'access_token': access_token, 'refresh_token': refresh_token}, status=200)


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
		if not user_info.get('id'):
			return JsonResponse({'message': 'TOKEN_NOT_VALID'}, status=405)
		if not user_info.get('properties'):
			return JsonResponse({'message': 'TOKEN_NOT_VALID'}, status=405)
		if not user_info.get('properties').get('nickname'):
			return JsonResponse({'message': 'TOKEN_NOT_VALID'}, status=405)
		user_id = login_site + '_' + str(user_info.get('id'))
		user_nickname = user_info.get('properties').get('nickname')

		return (user_id, user_nickname)
	except ValueError:
		pass
