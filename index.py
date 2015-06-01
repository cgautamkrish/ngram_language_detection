import codecs
import nltk
import collections
import operator

def getProbability(lang_list, key):
	counter = collections.Counter(lang_list)
	total_count = 0
	new_dict = {}
	for i in counter:
		total_count += counter[i]
	for g in counter:
		prob = float(counter[g]+1)/total_count
		new_dict[g] = prob
	return new_dict

def getFileContents(file_name):
	file_content = codecs.open(file_name, "r", "utf-8")
	return file_content

def getNgrams(line):
	length = len(line)
	tokens = []
	for i in range(0, length):
		ngram = ()
		if (i + 1) < length:
			ngram = (line[i], line[i+1])
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
indon = {}
malay = {}
tam = {}
othe = {}

lang_probabilities = {'indonesian' : indon, 'malaysian' : malay, 'tamil' : tam, 'others' : othe}
for key in lang_probabilities:
	lang_probabilities[key] = getProbability(lang_dict[key], key)
	# with open('langs.txt', 'a') as f:
	# 	for k in lang_probabilities[key]:
	# 		try:
	# 			f.write(' '.join(k))
	# 			f.write(' ')
	# 		except UnicodeEncodeError:
	# 			pass

# for i in lang_probabilities:
# 	print(lang_probabilities[i])

# Now test it on the test text data (input.test.txt)
test_file_contents = getFileContents('input.test.txt')

for line in test_file_contents:
	try:
		probability = {'indonesian' : 0, 'malaysian' : 0, 'tamil' : 0, 'others' : 0}
		tokens = nltk.word_tokenize(line)
		line_ngrams = getNgrams(tokens)
		for i in line_ngrams:
			for j in lang_probabilities:
				for item in lang_probabilities[j]:
					if i == item:
						if probability[j] == 0:
							probability[j] = lang_probabilities[j][item]
						else:
							probability[j] = probability[j] * lang_probabilities[j][item]
		likely_language = max(probability.items(), key=operator.itemgetter(1))[0]
		print("Detected language: " + likely_language)
	except UnicodeEncodeError:
		pass

