import os
import json

from sklearn import datasets
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB


def categorize(folder = 'keywords'):
	
	files = os.listdir(folder)
	
	container = 'categories'
	
	for file in files:
		data = json.load(open('/'.join([folder, file]), 'r'))
		questions = data['q_kw'].keys()
		
		cat_name = file.split('.json')[0]
		cat_folder = '/'.join([container, cat_name])
		if not os.path.exists(cat_folder):
			os.mkdir(cat_folder)
		with open('/'.join([cat_folder, 'file']), 'w') as f:
			for question in questions:
				f.write(question + '\n\n')
				


def create_dataset(container_path='categories'):
	dset = datasets.load_files(container_path)
	return dset


def train(dset):
	count_vect = CountVectorizer()
	X_train_counts = count_vect.fit_transform(dset.data)
	tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
	X_train_tf = tf_transformer.transform(X_train_counts)
	tfidf_transformer = TfidfTransformer()
	X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
	clf = MultinomialNB().fit(X_train_tfidf, dset.target)
	
	return (clf, count_vect, tfidf_transformer)

dset = create_dataset()
clf, count_vect, tfidf_transformer = train(dset)
docs_new = ['скульптуры', 'интересная и прикольная работа', 'как работает компьютер', 'расскажи анекдот про владимира путина']
X_new_counts = count_vect.transform(docs_new)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)

for doc, category in zip(docs_new, predicted):
    print('%r => %s' % (doc, dset.target_names[category]))
    

