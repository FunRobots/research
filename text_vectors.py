import math

class BadDimension(Exception):
	
	def __init__(self):
		self.msg = "BadDimension!"



class Vector:
	
	def __init__(self, vec_list):
		self.vec = vec_list
		
	def get(self):
		return self.vec
	
	def dim(self):
		return len(self.vec)
	
	def __abs__(self):
		sum = 0
		for coord in self.vec:
			sum += coord ** 2
		return math.sqrt(sum)
		
	def __getitem__(self, key):
		return self.vec[key]
		
	def __mul__(self, other):
		'''
		Scalar vectors product
		'''
		if len(self.vec) != other.dim():
			raise BadDimension
		i = 0
		scalar = 0
		while i < len(self.vec):
			scalar += self.vec[i] * other[i]
			i += 1
		return scalar
		
	

class TextVector:

	def __init__(self, text_units):
		self.text_units = text_units
		self._form_word_set()
		self._form_matrix()
				
	def _form_word_set(self):
		self._words = list()
		for unit in self.text_units:
			for word in unit:
				if word not in self._words:
					self._words.append(word)
	
	def _wordcount(self, word, unit):
		count = 0
		for unit_word in unit:
			if word == unit_word:
				count += 1
		return count
	
	def _unit2vec(self, unit):
		vec = []
		for word in self._words:
			vec.append(self._wordcount(word, unit))
		word_vector = Vector(vec)
		return word_vector
		
	def _form_matrix(self):
		self.matrix = []
		for unit in self.text_units:
			self.matrix.append(self._unit2vec(unit))
	
	def _cosine(self, v1, v2):
		'''
		v1, v2 : Vector
		'''
		return (v1 * v2) / (abs(v1) * abs(v2))
		
	def closest_units(self, phrase):
		'''
		phrase: list
		'''
		#phrase => Vector
		phrase_vector = self._unit2vec(phrase)
		cosines = []
		#find cosine similarities with all vectors
		for vector in self.matrix:
			cosines.append(self._cosine(vector, phrase_vector))
			
		#find maximum cosine similarity value index and form max cosine similarity value list
		max_cosine_similarity = max(cosines)
		matching_units = []
		index = 0
		while index < len(cosines):
			if cosines[index] == max_cosine_similarity:
				matching_units.append(self.text_units[index])
			index += 1
		return matching_units


unit1 = ['hello', 'how', 'are', 'you']
unit2 = ['what', 'is','the', 'weather']
unit3 = ['say', 'please', 'anecdote']

units = [unit1, unit2, unit3]
tv = TextVector(units)
M = tv.matrix
for vec in M:
	print(vec.get())
	
print(tv.closest_units(['say', 'please','is', 'the', 'weather']))
