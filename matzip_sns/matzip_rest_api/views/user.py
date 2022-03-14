import json
from django.contrib.auth.models import User
from matzip_rest_api.models.models import Userinfo
from matzip_rest_api.exception.exception import NotMatchAccessToken, NotMatchUserEval
from rest_framework.views import APIView
from matzip_rest_api.jwt_func import validate_token
from django.http import JsonResponse
from django.core import serializers

class UserView(APIView):
	# 다른 사용자의 정보는 얻을 수 있게
	def get(self, request):
		try:
			encoded_jwt = request.headers.get('Authorization', None)
			decoded_jwt = validate_token(encoded_jwt)
			if (decoded_jwt['token_type'] != "access_token"):
				raise NotMatchAccessToken

			user = User.objects.get(username=decoded_jwt['user_id'], last_name=decoded_jwt['nickname'])

			# another_user = User.objects.get(username=body['user_id'])
			# another_userinfo = Userinfo.objects.get(user=another_user)
			userinfo = serializers.serialize("json", Userinfo.objects.filter(user=user))

			return JsonResponse({'userinfo': userinfo, 'message': 'success'}, status=200)

		# 토큰에 원하는 값이 없을 경우
		except TypeError:
			return (JsonResponse({'message': 'TOKEN_INFO ERROR'}, status=400))
		# token_type이 accss_token 아닌경우 , token body 타입이 js 아닐때
		except NotMatchAccessToken:
			return (JsonResponse({'message': 'TOKEN_TYPE ERROR'}, status=400))
		# user - not exist
		except User.DoesNotExist:
			return (JsonResponse({'message': 'USER REQUITED'}, status=400))
		except json.decoder.JSONDecodeError:
			return (JsonResponse({'message': 'JSONDecodeError'}, status=400))

	def put(self, request):
		try:
			encoded_jwt = request.headers.get('Authorization', None)
			decoded_jwt = validate_token(encoded_jwt)
			if (decoded_jwt['token_type'] != "access_token"):
				raise NotMatchAccessToken

			body = json.loads(request.body.decode('utf-8'))

			user = User.objects.get(username=decoded_jwt['user_id'], last_name=decoded_jwt['nickname'])
			userinfo=Userinfo.objects.get(user=user)
			
			user.last_name = body['nickname']
			user.save()
			userinfo.introduce = body['introduce']
			userinfo.area = body['area']
			userinfo.save()

			return JsonResponse({'message': 'success, need NEW access_token'}, status=200)
			
		# 토큰에 원하는 값이 없을 경우
		except TypeError:
			return (JsonResponse({'message': 'TOKEN_INFO ERROR'}, status=400))
		# token_type이 accss_token 아닌경우 , token body 타입이 js 아닐때
		except NotMatchAccessToken:
			return (JsonResponse({'message': 'TOKEN_TYPE ERROR'}, status=400))
		# body - info not vaild
		except KeyError:
			return (JsonResponse({'message': 'body_info REQUITED'}, status=400))
		# Model - not exist
		except User.DoesNotExist:
			return (JsonResponse({'message': 'USER REQUITED'}, status=400))
	# def delete(self, request):
