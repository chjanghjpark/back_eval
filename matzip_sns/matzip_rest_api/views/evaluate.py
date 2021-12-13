import requests
import json
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from matzip_rest_api.jwt_func import validate_token
from django.contrib.auth.models import User
from matzip_rest_api.models.models import Evaluate
from django.http import JsonResponse
from django.core import serializers

@method_decorator(csrf_exempt, name='dispatch')
class EvaluateView(APIView):
	def post(self, request):
		# 유효하지 않은 jwt일 경우 예외사항 만들어야함.
		encoded_jwt = request.headers.get('Authorization', None)
		decoded_jwt = validate_token(encoded_jwt)
		user_id = decoded_jwt['user_id']
		user_nickname = decoded_jwt['nickname']

		body = json.loads(request.body.decode('utf-8'))
		eval_store = body['store']
		eval_star = body['star']

		eval_user = User.objects.get(username=user_id, password=user_id, last_name=user_nickname)
		eval = Evaluate.objects.create(store=eval_store, star=eval_star, user=eval_user)

		return JsonResponse({'message': 'success'}, status=200)

	def get(self, request):
		encoded_jwt = request.headers.get('Authorization', None)
		decoded_jwt = validate_token(encoded_jwt)
		user_id = decoded_jwt['user_id']
		user_nickname = decoded_jwt['nickname']

		eval_user = User.objects.get(username=user_id, password=user_id, last_name=user_nickname)

		eval = serializers.serialize("json", Evaluate.objects.filter(user=eval_user))
		return JsonResponse({'eval': eval, 'message': 'success'}, status=200)

	def put(self, request):
		encoded_jwt = request.headers.get('Authorization', None)
		decoded_jwt = validate_token(encoded_jwt)
		user_id = decoded_jwt['user_id']
		user_nickname = decoded_jwt['nickname']

		eval_user = User.objects.get(username=user_id, password=user_id, last_name=user_nickname)

		body = json.loads(request.body.decode('utf-8'))
		eval_pk = body['pk']
		eval_store = body['store']
		eval_star = body['star']

		# 다른 유저의 토큰으로 해당 유저의 글을 수정할 수 없음.
		eval_obj = Evaluate.objects.get(id=eval_pk)
		if (eval_user.username != str(eval_obj.user)):
			return (JsonResponse({'message': 'not match user to eval'}, status=400))

		eval_obj.store = eval_store
		eval_obj.star = eval_star
		eval_obj.save()

		eval = serializers.serialize("json", Evaluate.objects.filter(pk = eval_pk))
		return JsonResponse({'eval': eval, 'message': 'success'}, status=200)

	def delete(self, request):
		encoded_jwt = request.headers.get('Authorization', None)
		decoded_jwt = validate_token(encoded_jwt)
		user_id = decoded_jwt['user_id']
		user_nickname = decoded_jwt['nickname']

		eval_user = User.objects.get(username=user_id, password=user_id, last_name=user_nickname)

		body = json.loads(request.body.decode('utf-8'))
		eval_pk = body['pk']

		eval_obj = Evaluate.objects.get(id=eval_pk)
		if (eval_user.username != str(eval_obj.user)):
			return (JsonResponse({'message': 'not match user to eval'}, status=400))
		eval_obj.delete()
		return JsonResponse({'message': 'success'}, status=200)
