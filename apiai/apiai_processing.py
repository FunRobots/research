import apiai
import json
import random
from urllib import request

class Processor:
    def __init__(self,client_key, dev_key):
    	
        self.client_key = client_key
        self.dev_key = dev_key
        self._connect()
        self._make_session_id()
        
    def _make_session_id(self):

        symbols = '0123456789abcdef'
        self.session_id = ''
        for i in range(36):
            self.session_id += symbols[random.randint(0, len(symbols) - 1)]
    
    def _connect(self):
        self._ai = apiai.ApiAI(self.client_key)
        
    def add_intent(self, json_data):
        '''
        adds new intent to bot
        '''
        url = 'https://api.api.ai/v1/intents?v=20150910'
        header = {'Authorization': 'Bearer ' + self.dev_key,
                 'Content-Type': 'application/json; charset=utf-8'
                 }
                 
        q = request.Request(url=url, data=json.dumps(json_data).encode('utf-8'), headers=header)
        response = request.urlopen(q).read().decode('utf-8')
        return response
        
def main():
    processor = Processor(client_key='517ac0f88f924edcaab54504270338c0', dev_key='a528f4108c114a29988a59ee722905f2')
    intent = {
           'name': 'my test post',
           'auto': True,
           'contexts': [],
           'templates': [],
           'userSays': [
              {
                 'data': [
                    {
                       'text': 'как так-то '
                    }
                 ],
                 'isTemplate': False,
                 'count': 0
              }
           ],
           'responses': [
              {
                 'speech': 'как-то так '
              }
           ],
           'priority': 500000
    }
    print(processor.add_intent(intent))


if __name__ == '__main__':
    main()
