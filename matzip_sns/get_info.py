import requests
import json

ACCESS_TOKEN = ''
KAKAO_URL = "https://kapi.kakao.com/v2/user/me"

headers = {
	'Authorization': 'Bearer' + ' ' + ACCESS_TOKEN
}
response = requests.post(KAKAO_URL, headers=headers)
print(response)
# print(response.json())
User_Info = response.json()
user_id = User_Info.get('id')
user_nickname = User_Info.get('properties').get('nickname')
print(user_id, user_nickname)
