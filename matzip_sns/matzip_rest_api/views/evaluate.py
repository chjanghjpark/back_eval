import requests
import json
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from matzip_rest_api.jwt_func import validate_token
from django.contrib.auth.models import User
from matzip_rest_api.models.models import Evaluate, Store
from django.http import JsonResponse
from django.core import serializers
from django.core.exceptions import ValidationError
from matzip_rest_api.exception.exception import NotMatchAccessToken, NotMatchUserEval

@method_decorator(csrf_exempt, name='dispatch')
class EvaluateView(APIView):
	def post(self, request):
		try:
			encoded_jwt = request.headers.get('Authorization', None)
			decoded_jwt = validate_token(encoded_jwt)
			if (decoded_jwt['token_type'] != "access_token"):
				raise NotMatchAccessToken
			body = json.loads(request.body.decode('utf-8'))

			user = User.objects.get(
				username=decoded_jwt['user_id'], 
				last_name=decoded_jwt['nickname']
				)

			store, _ = Store.objects.get_or_create(
				place_id=body['id'],
				place_name=body['place_name'], 
				address_name=body['address_name'], 
				place_url=body['place_url'],
				phone=body['phone'],
				category_group_name=body['category_group_name'],
				category_group_code=body['category_group_code'],
				x=body['x'],
				y=body['y'],
				area=body['area'],
				district=body['district'],
				)
				
			eval = Evaluate.objects.create(
				user=user, 
				store=store, 
				star=int(body['star']), 
				content=body['content'],
				invited_date=body['invited_date'], 
				open_close=body['open_close']
				)
				
			eval_return = serializers.serialize("json", Evaluate.objects.filter(pk=eval.pk))
			return JsonResponse({'eval': eval_return, 'message': 'success'}, status=200)

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


	def get(self, request):
		try:
			encoded_jwt = request.headers.get('Authorization', None)
			decoded_jwt = validate_token(encoded_jwt)
			if (decoded_jwt['token_type'] != "access_token"):
				raise NotMatchAccessToken

			user = User.objects.get(username=decoded_jwt['user_id'], last_name=decoded_jwt['nickname'])
			eval = serializers.serialize("json", Evaluate.objects.filter(user=user), use_natural_foreign_keys=True)

			return JsonResponse({'eval': eval, 'message': 'success'}, status=200)

		# 토큰에 원하는 값이 없을 경우
		except TypeError:
			return (JsonResponse({'message': 'TOKEN_INFO ERROR'}, status=400))
		# token_type이 accss_token 아닌경우 , token body 타입이 js 아닐때
		except NotMatchAccessToken:
			return (JsonResponse({'message': 'TOKEN_TYPE ERROR'}, status=400))
		# user - not exist
		except User.DoesNotExist:
			return (JsonResponse({'message': 'USER REQUITED'}, status=400))

	def put(self, request):
		try:
			encoded_jwt = request.headers.get('Authorization', None)
			decoded_jwt = validate_token(encoded_jwt)
			if (decoded_jwt['token_type'] != "access_token"):
				raise NotMatchAccessToken

			body = json.loads(request.body.decode('utf-8'))

			# 다른 유저의 토큰으로 해당 유저의 글을 수정할 수 없음.
			user = User.objects.get(username=decoded_jwt['user_id'], last_name=decoded_jwt['nickname'])
			eval = Evaluate.objects.get(id=body['pk'])
			store = Store.objects.get(place_id=body['id'])
			if (user.username != str(eval.user)):
				raise NotMatchUserEval

			eval.store = store
			eval.star = int(body['star'])
			eval.invited_date=body['invited_date']
			eval.open_close=body['open_close']
			eval.content=body['content']
			eval.save()

			eval = serializers.serialize("json", Evaluate.objects.filter(pk=body['pk']))
			return JsonResponse({'eval': eval, 'message': 'success'}, status=200)

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
		except Store.DoesNotExist:
			return (JsonResponse({'message': 'Store REQUITED'}, status=400))
		except Evaluate.DoesNotExist:
			return (JsonResponse({'message': 'Evaluation REQUITED'}, status=400))
		# 글쓴이랑 실제 유저랑 다른경우
		except NotMatchUserEval:
			return (JsonResponse({'message': 'not match user to eval'}, status=400))
		except ValidationError:
			return (JsonResponse({'message': 'ValidationError'}, status=400))
		except json.decoder.JSONDecodeError:
			return (JsonResponse({'message': 'JSONDecodeError'}, status=400))

	def delete(self, request):
		try:
			encoded_jwt = request.headers.get('Authorization', None)
			decoded_jwt = validate_token(encoded_jwt)
			if (decoded_jwt['token_type'] != "access_token"):
				raise NotMatchAccessToken

			body = json.loads(request.body.decode('utf-8'))

			user = User.objects.get(username=decoded_jwt['user_id'], last_name=decoded_jwt['nickname'])
			eval = Evaluate.objects.get(id=body['pk'])
			if (user.username != str(eval.user)):
				raise NotMatchUserEval

			eval.delete()

			return JsonResponse({'message': 'success'}, status=200)

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
		except Evaluate.DoesNotExist:
			return (JsonResponse({'message': 'Evaluation REQUITED'}, status=400))
		# 글쓴이랑 실제 유저랑 다른경우
		except NotMatchUserEval:
			return (JsonResponse({'message': 'not match user to eval'}, status=400))
