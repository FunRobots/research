import os
import json

src_folder = 'otvets'
aiml_folder = 'aiml'

corpus_file = 'corpus.txt'

def punct_filter(string, additional_symbols=None):
	
	russian_symbols = set("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789 ")
	if not additional_symbols is None:
		russian_symbols.update(additional_symbols)
	filtered_string = ''
	for char in string:
		if char in russian_symbols:
			filtered_string += char
	return filtered_string


def form_aimls_and_corpus():
	corpus = []
	src_files = os.listdir(src_folder)
	for file in src_files:
		data = json.load(open(src_folder + '/' + file, 'r'))
		questions = data['questions']
		
		aiml_file_name = aiml_folder + '/' + file[:-5] + '.aiml'
		aiml_file = open(aiml_file_name, 'w')
		
		aiml_file.write('<?xml version=\"1.1\" encoding=\"UTF-8\"?>\n')
		for question in questions:
			pattern = question['qtext']
			corpus.append(pattern)
			aiml_file.write('<category>\n<pattern>' + punct_filter(pattern).upper() + '</pattern>\n<template>\n')
			answers = question['answers']
			aiml_file.write('<random>\n')
			for answer in answers:
				aiml_file.write('<li>' + answer['atext'] + '</li>\n')
			aiml_file.write('</random>\n</template>\n</category>\n\n')
		aiml_file.write('</aiml>')
		aiml_file.close()
		
	json.dump(obj=dict({'corpus': corpus}), fp=open(corpus_file, 'w'), ensure_ascii=False, indent=4)

form_aimls_and_corpus()
