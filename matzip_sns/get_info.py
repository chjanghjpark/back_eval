import requests
import json

KAKAO_TOKEN = ''

class Login():
	def post(ACCESS_TOKEN, login_site):
		url = "http://127.0.0.1:8000/login/"

		headers = {
			'Authorization': ACCESS_TOKEN
		}
		data = {
			'login_site': login_site
		}
		response = requests.post(url, headers=headers, data=json.dumps(data))
		print(response)

		user_info = response.json()
		access_token = user_info.get('access_token')
		refresh_token = user_info.get('refresh_token')
		return access_token, refresh_token

	def get(refresh_token):
		url = "http://127.0.0.1:8000/login/"
		headers = {
			'Authorization': refresh_token
		}
		response = requests.get(url, headers=headers)
		print(response)
		
		user_info = response.json()
		access_token = user_info.get('access_token')
		return access_token

class Eval():
	def post(access_token):
		url = "http://127.0.0.1:8000/eval/"

		headers = {
			'Authorization': access_token,
		}
		data = {
			'store': 'test123',
			'star': '1',
		}
		response = requests.post(url, headers=headers, data=json.dumps(data))
		print(response)

		message_json = response.json()
		message = message_json.get('message')
		return message

	def get(access_token):
		url = "http://127.0.0.1:8000/eval/"

		headers = {
			'Authorization': access_token,
		}

		response = requests.get(url, headers=headers)
		print(response)

		message_json = response.json()
		message = message_json.get('eval')
		return message

	def put(access_token):
		url = "http://127.0.0.1:8000/eval/"

		headers = {
			'Authorization': access_token,
		}
		data = {
			'pk': 16,
			'store': 'front',
			'star': '5',
		}

		response = requests.put(url, headers=headers, data=json.dumps(data))
		print(response)

		message_json = response.json()
		message = message_json.get('eval')
		return message

	def delete(access_token, pk):
		url = "http://127.0.0.1:8000/eval/"

		headers = {
			'Authorization': access_token,
		}
		data = {
			'pk': pk,
		}

		response = requests.delete(url, headers=headers, data=json.dumps(data))
		print(response)

		message_json = response.json()
		message = message_json.get('message')
		return message



access_token, refresh_token = Login.post(KAKAO_TOKEN, 'kakao')
print(access_token)
access_token = Login.get(refresh_token)
print(access_token)
# message = Eval.post(access_token)
# message = Eval.get(access_token)
# print(message)
# message = Eval.put(access_token)
# message = Eval.delete(access_token, 9)
# print(message)
