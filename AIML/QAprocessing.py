import argparse
import os
import json
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


class QABaseProcessor:
			
	def _create_aiml_folder(self, aiml_folder):
		if not os.path.exists(aiml_folder):
			os.mkdir(aiml_folder)
	
	def _punct_filter(self, string, additional_symbols=None):
	
		russian_symbols = set("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789 ")
		if not additional_symbols is None:
			russian_symbols.update(additional_symbols)
		filtered_string = ''
		for char in string:
			if char in russian_symbols:
				filtered_string += char
		return filtered_string
	
	def create_corpus_and_aiml(self, src_folder, corpus_file, aiml_folder):
		self._create_aiml_folder(aiml_folder)
		corpus = []
		src_files = os.listdir(src_folder)
		for file in src_files:
			data = json.load(open(src_folder + '/' + file, 'r'))
			questions = data['questions']
			
			aiml_file_name = aiml_folder + '/' + file[:-5] + '.aiml'
			aiml_file = open(aiml_file_name, 'w')
		
			aiml_file.write('<?xml version=\"1.1\" encoding=\"UTF-8\"?>\n<aiml version=\"2.0\">\n')
			for question in questions:
				pattern = self._punct_filter(question['qtext'])
				corpus.append(pattern)
				aiml_file.write('<category>\n<pattern>' + pattern.upper() + '</pattern>\n<template>\n')
				answers = question['answers']
				aiml_file.write('<random>\n')
				for answer in answers:
					aiml_file.write('<li>' + self._punct_filter(answer['atext']) + '</li>\n')
				aiml_file.write('</random>\n</template>\n</category>\n\n')
			aiml_file.write('</aiml>')
			aiml_file.close()
		
		json.dump(obj=dict({'corpus': corpus}), fp=open(corpus_file, 'w'), ensure_ascii=False, indent=4)
		

def main(src_folder='otvets', corpus_file='corpus.txt', aiml_folder='aiml'):
	processor = QABaseProcessor()
	processor.create_corpus_and_aiml(src_folder, corpus_file, aiml_folder)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--src_folder', dest='src_folder')
	parser.add_argument('--corpus_file', dest='corpus_file')
	parser.add_argument('--aiml_folder', dest='aiml_file')
	args = parser.parse_args()
	
	main(args.src_folder, args.corpus_file, args.aiml_file)
