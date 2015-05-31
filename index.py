import codecs
import nltk
import collections

def getProbability(lang_list):
	counter = collections.Counter(lang_list)
	length_ngrams = len(counter.values()) 
	list_of_probs = [(i+1) for i in counter.values()]
	probability_list = [(i/float(length_ngrams)) for i in list_of_probs]
	return probability_list

file_content = codecs.open('input.train.txt', "r", "utf-8")

indonesian = [('','','','')]
malaysian = [('','','','')]
tamil = [('','','','')]
others = [('','','','')]

lang_dict = {'indonesian' : indonesian, 'malaysian' : malaysian, 'tamil' : tamil, 'others' : others}

for line in file_content:
	try:
		tokens = nltk.word_tokenize(line)
		language = tokens[0]
		del tokens[0]
		ngram = zip(*(iter(tokens),) *4)
		lang_dict[language] += ngram
	except UnicodeEncodeError:
		pass

# Get probabilites for each language
lang_probabilities = {'indonesian' : indonesian, 'malaysian' : malaysian, 'tamil' : tamil, 'others' : others}
for key in lang_dict:
	lang_probabilities[key] = getProbability(lang_dict[key])
