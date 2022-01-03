class NotMatchUserEval(Exception):
	def __init__(self):
		super().__init__('NotMatchUserEval')

class NotMatchAccessToken(Exception):
	def __init__(self):
		super().__init__('NotMatchAccessToken')
