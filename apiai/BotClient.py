import apiai
import random
import json

class APIAIBot:
	'''
	simple bot class based on apiai
	'''
	
	def __init__(self,client_key):
		self.client_key = client_key
		self._make_session_id()
		self._connect()
		
	def _make_session_id(self):
		'''
		creates session_id
		'''
		symbols = '0123456789abcdef'
		self.session_id = ''
		for i in range(36):
		    self.session_id += symbols[random.randint(0, len(symbols) - 1)]
    
	def _connect(self):
		'''
		connects to api.ai
		'''
		self._ai = apiai.ApiAI(self.client_key)
		
	def request(self, msg):
		'''
		makes request and returns response from api.ai bot
		'''
		req = self._ai.text_request()
		req.lang = 'ru'
		req.session_id = self.session_id
		req.query = msg
		response = json.loads(req.getresponse().read().decode('utf-8'))
		
		return response['result']['fulfillment']['speech']

		
	def _parse_intent(self, intent):
		pass
		

def main():

	bot = APIAIBot(client_key='517ac0f88f924edcaab54504270338c0')
	msg = ''
	while msg != 'stop':
		msg = input('>')
		response = bot.request(msg)
		print(response)
		
if __name__ == '__main__':
	main()
	
