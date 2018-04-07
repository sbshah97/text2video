# coding=utf-8
import nltk
from nltk.collocations import *
import unicodedata
import json
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import httplib, urllib, base64

MAX_STRINGS_IN_SEARCH_QUERY = 3

# just considering history related events. Following tags according to NLTK 
# are important which defines the sentences.
import_tags = [
	'FW', 'NN', 'NNS', 'NNP', 'NNPS', 'CD'
]

corpus = '''During World War II, the United States and the Soviet Union fought together as allies against the Axis powers. However, the relationship between the two nations was a tense one. Americans had long been wary of Soviet communism and concerned about Russian leader Joseph Stalin’s tyrannical, blood-thirsty rule of his own country. For their part, the Soviets resented the Americans’ decades-long refusal to treat the USSR as a legitimate part of the international community as well as their delayed entry into World War II, which resulted in the deaths of tens of millions of Russians. After the war ended, these grievances ripened into an overwhelming sense of mutual distrust and enmity. Postwar Soviet expansionism in Eastern Europe fueled many Americans’ fears of a Russian plan to control the world. Meanwhile, the USSR came to resent what they perceived as American officials’ bellicose rhetoric, arms buildup and interventionist approach to international relations. In such a hostile atmosphere, no single party was entirely to blame for the Cold War; in fact, some historians believe it was inevitable.'''
stopset = set(stopwords.words('english'))
stopset.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}'])

def tokenize_sentences(sentences):
	sentence_tokenlize_list = sent_tokenize(sentences)
	print "Number of sentences in the input text: " + str(len(sentence_tokenlize_list))
	return sentence_tokenlize_list

def word_tokenized_sentences(tokenized_sentences):
	word_tokenized_sentences = []
	for sent in tokenized_sentences:
		tokens = word_tokenize(str(sent))
		modified_tokens = []
		for token in tokens:
			token = str(unicode(token, 'ascii', 'ignore'))
			if token.lower() not in stopset:
				modified_tokens.append(token)
		word_tokenized_sentences.append(modified_tokens)
	return word_tokenized_sentences

def query_tokens(word_tokenized_sentences):
	query_tokens = []
	for tokens in word_tokenized_sentences:
		tagged_tokens = nltk.pos_tag(tokens)
		query_token = []
		for word, tag in tagged_tokens:
			if tag in import_tags:
				query_token.append(word)
		query_tokens.append(query_token)
		#print query_token
	return query_tokens

# Bigrams not really useful.
def bigram_finders(query_tokens):
	important_words = [token for tokens in query_tokens for token in tokens]
	important_words = list(set(important_words))
	bigram_measures = nltk.collocations.BigramAssocMeasures()
	finder = BigramCollocationFinder.from_words(important_words)
	#print finder.nbest(bigram_measures.pmi, 10)

def term_frequency(corpus):
	# Term frequency.
	tf = []
	lower_corpus = corpus.lower()
	for word in important_words:
		count_ = lower_corpus.count(word)
		tf.append((word, count_))
	tf = sorted(tf, key=lambda x: x[1])
	#print tf

def bing_text_analysis(tokenized_sentences):
	headers = {
	    # Request headers
	    'Content-Type': 'application/json',
	    'Ocp-Apim-Subscription-Key': '230f2b84e2bd4c119d1858334627069e',
	}
	params = urllib.urlencode({
		# Request parameters
		'numberOfLanguagesToDetect': '1',
	})
	sentences = []
	for sentence in tokenized_sentences:
		sentence_ = ""
		for word in sentence.split(' '):
			token = unicode(word, 'ascii', 'ignore')
			sentence_ += token + " "
		# print sentence_
		sentences.append(sentence_)
	try:
		body = {}
		body['documents'] = []
		id_counter = 1
		for sentence in sentences:
			document = {}
			document['id'] = id_counter
			document['text'] = str(sentence)
			id_counter += 1
			body['documents'].append(document)
		# print str(body)

		conn = httplib.HTTPSConnection('australiaeast.api.cognitive.microsoft.com')
		conn.request("POST", "/text/analytics/v2.0/keyPhrases", str(body), headers)
		response = conn.getresponse()
		data = response.read()
		conn.close()
		data = json.loads(data)
		print data
		return data, sentences
	except Exception as e:
	    print(e)

def fetch_search_queries(corpus):
	bing_results, sentences = bing_text_analysis(tokenize_sentences(corpus))
	# print bing_results
	query_results = query_tokens(word_tokenized_sentences(tokenize_sentences(corpus)))
	# print query_results

	# print len(bing_results), len(query_results)
	ind_counter = 0
	search_queries = []
	bing_results = dict(bing_results)
	for results in bing_results['documents']:
		# print results
		list_of_imp_words = query_results[ind_counter]
		# print list_of_imp_words
		ind_counter += 1
		imp_words = []
		for word in results['keyPhrases']:
			list_words = word.split(' ')
			keep_word = True
			for word_ in list_words:
				# print word_
				if str(word_) not in list_of_imp_words:
					keep_word = False
			if keep_word:
				imp_words.append(str(word))
		search_query = ""
		word_number_query = 0
		for word in imp_words:
			if word_number_query >= MAX_STRINGS_IN_SEARCH_QUERY:
				break
			word_number_query += 1
			search_query += word + " "
		search_queries.append(search_query)
	return search_queries, sentences

def summarize(text):
	tokenized_sentences = tokenize_sentences(text)
	

# returns search queries and sentences used to create them. Use these sentences in TTS
search_queries, sentences = fetch_search_queries(corpus)

print search_queries