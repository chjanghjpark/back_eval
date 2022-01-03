import json
from django.contrib.auth.models import User
from matzip_rest_api.models.models import Userinfo
from matzip_rest_api.exception.exception import NotMatchAccessToken, NotMatchUserEval
from rest_framework.views import APIView
from matzip_rest_api.jwt_func import validate_token
from django.http import JsonResponse
from django.core import serializers

class UserView(APIView):
	def get(self, request):
		try:
			encoded_jwt = request.headers.get('Authorization', None)
			decoded_jwt = validate_token(encoded_jwt)
			if (decoded_jwt['token_type'] != "access_token"):
				raise NotMatchAccessToken

			user = User.objects.get(username=decoded_jwt['user_id'], last_name=decoded_jwt['nickname'])
			userinfo = serializers.serialize("json", Userinfo.objects.filter(user=user))

			return JsonResponse({'userinfo': userinfo, 'message': 'success'}, status=200)

		except:
			pass
	def put(self, request):
		try:
			encoded_jwt = request.headers.get('Authorization', None)
			decoded_jwt = validate_token(encoded_jwt)
			if (decoded_jwt['token_type'] != "access_token"):
				raise NotMatchAccessToken

			body = json.loads(request.body.decode('utf-8'))

			user = User.objects.get(username=decoded_jwt['user_id'], last_name=decoded_jwt['nickname'])
			userinfo=Userinfo.objects.get(user=user)
			
			userinfo.introduce = body['introduce']
			userinfo.area = body['area']
			userinfo.save()

			userinfo = serializers.serialize("json", Userinfo.objects.filter(user=user))
			return JsonResponse({'userinfo': userinfo, 'message': 'success'}, status=200)
		except:
			pass
	# def delete(self, request):
