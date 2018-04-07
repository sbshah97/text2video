# coding=utf-8
from imports import *

MAX_STRINGS_IN_SEARCH_QUERY = 3

# just considering history related events. Following tags according to NLTK
# are important which defines the sentences.
import_tags = [
	'FW', 'NN', 'NNS', 'NNP', 'NNPS', 'CD'
]

corpus = '''The Cold War was a state of geopolitical tension after World War II between powers in the Eastern Bloc (the Soviet Union and its satellite states) and powers in the Western Bloc (the United States, its NATO allies and others). Historians do not fully agree on the dates, but a common timeframe is the period between 1947, the year the Truman Doctrine, a U.S. foreign policy pledging to aid nations threatened by Soviet expansionism, was announced, and either 1989, when communism fell in Eastern Europe, or 1991, when the Soviet Union collapsed. The term "cold" is used because there was no large-scale fighting directly between the two sides, but they each supported major regional wars known as proxy wars.
The Cold War split the temporary wartime alliance against Nazi Germany, leaving the Soviet Union and the United States as two superpowers with profound economic and political differences. The USSR was a Marxist–Leninist state led by its Communist Party, which in turn was dominated by a leader with different titles over time, and a small committee called the Politburo. The Party controlled the press, the military, the economy and many organizations. It also controlled the other states in the Eastern Bloc, and funded Communist parties around the world, sometimes in competition with Communist China, particularly following the Sino-Soviet split of the 1960s. In opposition stood the capitalist West, led by the United States, a federal republic with a two-party presidential system. The First World nations of the Western Bloc were generally liberal democratic with a free press and independent organizations, but were economically and politically entwined with a network of banana republics and other authoritarian regimes throughout the Third World, most of which were the Western Bloc's former colonies.[1][2] Some major Cold War frontlines such as Vietnam, Indonesia, and the Congo were still Western colonies in 1947.
A small neutral bloc arose with the Non-Aligned Movement; it sought good relations with both sides. The two superpowers never engaged directly in full-scale armed combat, but they were heavily armed in preparation for a possible all-out nuclear world war. Each side had a nuclear strategy that discouraged an attack by the other side, on the basis that such an attack would lead to the total destruction of the attacker—the doctrine of mutually assured destruction (MAD). Aside from the development of the two sides' nuclear arsenals, and their deployment of conventional military forces, the struggle for dominance was expressed via proxy wars around the globe, psychological warfare, massive propaganda campaigns and espionage, rivalry at sports events, and technological competitions such as the Space Race.'''
stopset = set(stopwords.words('english'))
stopset.update(['.', ',', '"', "'", '?', '!', ':',
                ';', '(', ')', '[', ']', '{', '}'])

# Tokenising all sentences 
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
'''
Note:
Bigrams not really useful.
'''
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
	query_results = query_tokens(
		word_tokenized_sentences(tokenize_sentences(corpus)))
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