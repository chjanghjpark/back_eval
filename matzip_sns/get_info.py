import requests
import json

def get_info(ACCESS_TOKEN):

	KAKAO_URL = "https://kapi.kakao.com/v2/user/me"

	headers = {
		'Authorization': 'Bearer' + ' ' + ACCESS_TOKEN
	}
	response = requests.post(KAKAO_URL, headers=headers)
	print(response)
	# print(response.json())
	User_info = response.json()
	user_id = User_info.get('id')
	user_nickname = User_info.get('properties').get('nickname')
	print(user_id, user_nickname)
	return User_info

def get_info_backend(ACCESS_TOKEN):
	url = "http://127.0.0.1:8000/kakao_api/"

	headers = {
		'Authorization': ACCESS_TOKEN
	}
	response = requests.post(url, headers=headers)
	print(response)
	user_info = response.json()
	access_token = user_info.get('access_token')
	return access_token

def post_eval(backend_token):
	url = "http://127.0.0.1:8000/post/"

	headers = {
		'Authorization': 'Token ' + backend_token,
		'store': 'test',
		'star': '5',
	}
	response = requests.post(url, headers=headers)
	print(response)

ACCESS_TOKEN = 'O0Y07TBVSnNka2kdrBOiF2AB84OTdXTcbqz7ogopdSkAAAF82vKjSw'
# get_info(ACCESS_TOKEN)
backend_token = get_info_backend(ACCESS_TOKEN)
print(backend_token)
post_eval(backend_token)
