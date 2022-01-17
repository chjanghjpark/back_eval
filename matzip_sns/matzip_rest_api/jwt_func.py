import jwt
from rest_framework import status
import datetime

SECRET_PRE = ''

def	create_access_token(user, userinfo):
	encoded = jwt.encode(
		{
			'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
			'user_id' : user.username,
			'nickname': user.last_name,
			'introduce': userinfo.introduce,
			'area': userinfo.area,
			'login_site': userinfo.login_site,
			'token_type': 'access_token',
		},
		SECRET_PRE, algorithm='HS256'
	)
	return encoded

def create_refresh_token(user):
	encoded = jwt.encode(
		{
			'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
			'user_id' : user.username,
			'nickname': user.last_name,
			'token_type': 'refresh_token',
		},
		SECRET_PRE, algorithm='HS256'
	)
	return encoded

def validate_token(token):
	try:
		jwt.decode(token, SECRET_PRE, algorithms=['HS256'])
	# 토큰 만료
	except jwt.ExpiredSignatureError:
		return status.HTTP_401_UNAUTHORIZED
	except jwt.InvalidTokenError:
		return status.HTTP_401_UNAUTHORIZED
	else:
		return jwt.decode(token, SECRET_PRE, algorithms=['HS256'])

# kakao_token = 'kakaos'
# id = '12345'
# nickname = 'nicks'

# token = create_token(kakao_token, id, nickname)
# print(token)
# result = validate_token(token, kakao_token)
# print(result)

# https://jwt.io
# encoded_jwt = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")
# print(encoded_jwt)

# decoded_jwt = jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
# print(decoded_jwt)

# 카카오 토큰 + 시크릿 토큰을 같이 쓸지는 고민좀
