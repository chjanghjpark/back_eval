
import requests
import json
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from matzip_rest_api.jwt_func import validate_token
from django.contrib.auth.models import User
from matzip_rest_api.models.models import Evaluate, Comment
from django.http import JsonResponse
from django.core import serializers
from django.core.exceptions import ValidationError
from matzip_rest_api.exception.exception import NotMatchAccessToken, NotMatchUserEval

@method_decorator(csrf_exempt, name='dispatch')
class CommentView(APIView):
	def post(self, request):
		try:
			encoded_jwt = request.headers.get('Authorization', None)
			decoded_jwt = validate_token(encoded_jwt)
			if (decoded_jwt['token_type'] != "access_token"):
				raise NotMatchAccessToken
			body = json.loads(request.body.decode('utf-8'))

			user = User.objects.get(username=decoded_jwt['user_id'], last_name=decoded_jwt['nickname'])
			eval = Evaluate.objects.get(pk=body['pk'])
			comment = Comment.objects.create(user=user, evaluate=eval, content=body['content'])
			comment_return = serializers.serialize("json", Comment.objects.filter(pk=comment.pk))
			return JsonResponse({'comment': comment_return, 'message': 'success'}, status=200)

		# 토큰에 원하는 값이 없을 경우
		except TypeError:
			return (JsonResponse({'message': 'TOKEN_INFO ERROR'}, status=400))
		# token_type이 accss_token 아닌경우 , token body 타입이 js 아닐때
		except NotMatchAccessToken:
			return (JsonResponse({'message': 'TOKEN_TYPE ERROR'}, status=400))
		# body - info not vaild
		except KeyError:
			return (JsonResponse({'message': 'body_info REQUITED'}, status=400))
		# user - not exist
		except User.DoesNotExist:
			return (JsonResponse({'message': 'USER REQUITED'}, status=400))
		except ValidationError:
			return (JsonResponse({'message': 'ValidationError'}, status=400))
		except json.decoder.JSONDecodeError:
			return (JsonResponse({'message': 'JSONDecodeError'}, status=400))
