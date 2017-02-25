from rutermextract import TermExtractor
import os
import json
def get_keywords(text):
	keywords = []
	
	term_extractor = TermExtractor()
	for term in term_extractor(text):
		keywords.append(term.normalized)
	return keywords
		
		
if __name__ == '__main__':
	
	files = os.listdir('otvets')
	files_number = len(files)
	file_count = 1
	
	for file in files:
		q_kw = dict()
		data = json.load(open('otvets' + '/' + file, 'r'))
		questions = data['qestions']
		for question in questions:
			q_kw[question['qtext']] = get_keywords(question['qtext'])
			#print(q_kw)

		json.dump(obj=dict({'q_kw': q_kw}), fp=open('keywords/' + file, 'w'), ensure_ascii=False, indent=4)
