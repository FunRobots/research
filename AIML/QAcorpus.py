import json
import os

def create_qa_corpus(src_folder, qa_corpus_name):
	
	files = os.listdir(src_folder)
	
	for file in files:
		data = json.load(open(src_folder + '/' + file, 'r'))
		questions = data['questions']
		for question in questions:
			answers = question['answers']
			for answer in answers:
				qa = dict()
				qa[question['qtext']] = answer['atext']
				json.dump(obj=qa, fp=open(qa_corpus_name,'a'), ensure_ascii=False, indent=1)

create_qa_corpus(src_folder='otvets', qa_corpus_name='QAcorpus.txt')
