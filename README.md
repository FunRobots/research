# research
Temorary (raw) code sources


1. QAprocessing usage:
	
	python3 QAprocessing.py --src_folder src_folder --corpus_file corpus_file --aiml_folder aiml_folder
	
	src_folder - folder, which contains json files with questions and answers (for example, folder otvets)
	
	corpus_file - file name for corpus that will be built by this script
	
	aiml_folder - folder name for aiml scripts that will be built by this script
	
-----------------------------------------------------------------------------------------------------------

2. PBot usage:

	python3 PBot.py --corpus corpus --vtype vtype --aiml_folder aiml_folder
	
	corpus - file name for corpus that will be built by this script
	
	vtype - type of vectorizer, which with help vector of phrases builds; can take values : c - CountVectorizer , tfidf - TfidfVectorizer
	
	aiml_folder - folder name for aiml scripts that will be built by this script
	
------------------------------------------------------------------------------------------------------------
