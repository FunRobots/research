import os
import json
import argparse
import math
import aiml
import sys
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

class Bot:

    def __init__(self, aiml_folder):
        self.kernel = aiml.Kernel()
        self.base_path = sys.path[0]
        self._aiml_folder = aiml_folder
        self._learn()

    def _learn(self):
        files = os.listdir('/'.join([self.base_path, self._aiml_folder]))
        for file in files:
            if file[-4:] == 'aiml':
                print(file)
                self.kernel.learn('/'.join([self.base_path,self._aiml_folder,file]))

    def respond(self,qst=''):
        return self.kernel.respond(qst)


class PhraseAnalyzer:

	def __init__(self, corpus, vectorizer_type):
		self.corpus = corpus
		if vectorizer_type == 'c':
			self.vectorizer = CountVectorizer()
		if vectorizer_type == 'tfidf':
			self.vectorizer = TfidfVectorizer()
		
		self.X = self.vectorizer.fit_transform(self.corpus)
		self.matrix = self.X.toarray()
				
	
	def _abs(self, vec):
		sum = 0
		for coord in vec:
			sum += coord ** 2
		return math.sqrt(sum)
	
	def _cosine(self, v1, v2):
		if len(v1) == len(v2):
			scalar = 0
			i = 0
			while i < len(v1):
				scalar += v1[i] * v2[i]
				i += 1
			return scalar / (self._abs(v1) * self._abs(v2))
		return None
		
	def _nearest_vectors(self, vec):
		cosines = []
		for v in self.matrix:
			cosines.append(self._cosine(v, vec))
		max_cosine = max(cosines)
		
		#numbers of vectors
		vectors = []
		i = 0
		
		while i < len(cosines):
			if cosines[i] == max_cosine:
				vectors.append(i)
			i += 1
		return vectors
	
	def nearest_phrases(self, phrase):
		
		phrase_vec = self.vectorizer.transform([phrase]).toarray()
		vec_nums = self._nearest_vectors(phrase_vec[0])
		
		result = []
		for i in vec_nums:
			result.append(self.corpus[i])
		return result
		
	
class PredictiveBot:
	
	def __init__(self, corpus_file, vectorizer_type, aiml_folder):
		self.corpus = json.load(open(corpus_file, 'r'))['corpus']
		self.phrase_analyzer = PhraseAnalyzer(self.corpus, vectorizer_type)
		
		self.bot = Bot(aiml_folder)
		
		self.log_name = 'PBot.log'
		
	def request(self, phrase):
		nearest_phrases = self.phrase_analyzer.nearest_phrases(phrase)
		if len(nearest_phrases) == 1:
			print('nearest_phrase:', nearest_phrases[0])
			return self.bot.respond(nearest_phrases[0])
		else:
			json.dump(obj=dict({phrase: nearest_phrases}), fp=open(self.log_name, 'a'), ensure_ascii=False)
			return('Too many variants. See log.')
		

def main(corpus, vtype, aiml_folder):
	pbot = PredictiveBot(corpus, vtype, aiml_folder)
	msg = ''
	while msg != 'stop':
		msg = input('>')
		print(pbot.request(msg))
		
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--corpus', dest='corpus')
	parser.add_argument('--vtype', dest='vtype')
	parser.add_argument('--aiml_folder', dest='aiml_folder')
	args = parser.parse_args()
		
	main(args.corpus, args.vtype, args.aiml_folder)
