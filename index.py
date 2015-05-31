import codecs
import nltk
import collections

def getProbability(lang_list, key):
	counter = collections.Counter(lang_list)
	length_ngrams = len(counter.values()) 
	list_of_probs = [(i+1) for i in counter.values()]
	probability_list = [(i/float(length_ngrams)) for i in list_of_probs]
	with open("prob.txt", "a") as g:
		g.write(str(length_ngrams) + ' : ' + key)
		g.write('\n')
		count = 0
		for l,k in counter.items():
			count += 1
		g.write(str(count))
		g.write('\n')
	return probability_list

def getFileContents(file_name):
	file_content = codecs.open(file_name, "r", "utf-8")
	return file_content

def getNgrams(line):
	length = len(line)
	tokens = []
	for i in range(0, length):
		ngram = ()
		if (i + 3) < length:
			ngram = (line[i], line[i+1], line[i+2], line[i+3])
			tokens.append(ngram)
	return tokens

indonesian = []
malaysian = []
tamil = []
others = []

lang_dict = {'indonesian' : indonesian, 'malaysian' : malaysian, 'tamil' : tamil, 'others' : others}

file_content = getFileContents('input.train.txt')
for line in file_content:
	try:
		tokens = nltk.word_tokenize(line)
		language = tokens[0]
		del tokens[0]
		ngrams = getNgrams(tokens)
		for gram in ngrams:
			lang_dict[language].append(gram)
	except UnicodeEncodeError:
		pass

for key,value in lang_dict.items():
	with open('stuff.txt', 'a') as f:
		f.write('\n')
		f.write(key)
		f.write('\n')
		for k in value:
			try:
				f.write(' '.join(k))
				f.write(' ')
			except UnicodeEncodeError:
				pass

# Get probabilites for each language
indon = []
malay = []
tam = []
othe = []

lang_probabilities = {'indonesian' : indon, 'malaysian' : malay, 'tamil' : tam, 'others' : othe}
for key in lang_dict:
	# print(lang_dict[key])
	lang_probabilities[key] = getProbability(lang_dict[key], key)
	with open('langs.txt', 'a') as f:
		for k in lang_dict[key]:
			try:
				f.write(' '.join(k))
				f.write(' ')
			except UnicodeEncodeError:
				pass

# for i in lang_probabilities:
# 	print(lang_probabilities[i])

# Now test it on the test text data (input.test.txt)
test_file_contents = getFileContents('input.test.txt')

for line in test_file_contents:
	try:
		probability = {'indonesian' : 1, 'malaysian' : 1, 'tamil' : 1, 'others' : 1}
		tokens = nltk.word_tokenize(line)
		line_ngrams = getNgrams(tokens)
		# print(line_ngrams)
		for i in line_ngrams:
			for key,value in lang_dict.items():
				for idx,item in enumerate(value):
					if i == item:
						print(i)
						probability[key] = probability[key] * lang_probabilities[key][idx]
		print(probability)

		# with open("all_items.txt", "a") as d:
		# 	for single_ngram in line_ngrams:
		# 		print(single_ngram)
		# 		with open("test_tokens.txt", "a") as h:
		# 			h.write(str(single_ngram))
		# 			h.write('\n')
		# 		for key,value in lang_dict.items():
		# 			for idx,item in enumerate(value):
		# 				d.write(str(item))
		# 				d.write('\n')
		# 				if item == single_ngram:
		# 					#print(item)
		# 					probability[key] = probability[key] * lang_probabilities[key][idx]
		# print(probability)
	except UnicodeEncodeError:
		pass
