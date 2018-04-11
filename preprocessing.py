# coding=utf-8
from imports import *

MAX_STRINGS_IN_SEARCH_QUERY = 3

# just considering history related events. Following tags according to NLTK
# are important which defines the sentences.
import_tags = [
	'FW', 'NN', 'NNS', 'NNP', 'NNPS', 'CD'
]

# corpus = '''During World War II, the United States and the Soviet Union fought together as allies against the Axis powers. However, the relationship between the two nations was a tense one. Americans had long been wary of Soviet communism and concerned about Russian leader Joseph Stalin’s tyrannical, blood-thirsty rule of his own country. For their part, the Soviets resented the Americans’ decades-long refusal to treat the USSR as a legitimate part of the international community as well as their delayed entry into World War II, which resulted in the deaths of tens of millions of Russians. After the war ended, these grievances ripened into an overwhelming sense of mutual distrust and enmity. Postwar Soviet expansionism in Eastern Europe fueled many Americans’ fears of a Russian plan to control the world. Meanwhile, the USSR came to resent what they perceived as American officials’ bellicose rhetoric, arms buildup and interventionist approach to international relations. In such a hostile atmosphere, no single party was entirely to blame for the Cold War; in fact, some historians believe it was inevitable.'''
corpus = '''Subhash Chandra Bose was one of the most celebrated freedom fighters of India. He was a charismatic influencer of the youth and earned the epithet ‘Netaji’ by establishing and leading the Indian National Army (INA) during India’s struggle for independence. Although initially aligned with the Indian National Congress, he was ousted from the party due to his difference in ideology. He sought assistance from Nazi leadership in Germany and Imperial forces in Japan during the World War II, to overthrow the British from India. His sudden disappearance post 1945, led to surfacing of various theories, concerning the possibilities of his survival. '''
# corpus = '''Lodi Dynasty was the last dynasty of Delhi Sultanate and ruled from 1451 AD to 1526 AD. The Lodi Dynasty was of Afghan origin and Bahlul Lodi was the founder of Lodi Dynasty. In 1451 AD, Alam Shah, the last ruler of Sayyid Dynasty voluntarily abandoned the throne of Delhi Sultanate in favour of Bahlul Lodi. In 1526 AD, the Lodi Dynasty came to end after the first Battle of Panipat and marked the beginning of Mughal Empire.'''
# corpus = '''The Cold War was a state of geopolitical tension after World War II between powers in the Eastern Bloc (the Soviet Union and its satellite states) and powers in the Western Bloc (the United States, its NATO allies and others). Historians do not fully agree on the dates, but a common timeframe is the period between 1947, the year the Truman Doctrine, a U.S. foreign policy pledging to aid nations threatened by Soviet expansionism, was announced, and either 1989, when communism fell in Eastern Europe, or 1991, when the Soviet Union collapsed. The term "cold" is used because there was no large-scale fighting directly between the two sides, but they each supported major regional wars known as proxy wars.
# The Cold War split the temporary wartime alliance against Nazi Germany, leaving the Soviet Union and the United States as two superpowers with profound economic and political differences. The USSR was a Marxist–Leninist state led by its Communist Party, which in turn was dominated by a leader with different titles over time, and a small committee called the Politburo. The Party controlled the press, the military, the economy and many organizations. It also controlled the other states in the Eastern Bloc, and funded Communist parties around the world, sometimes in competition with Communist China, particularly following the Sino-Soviet split of the 1960s. In opposition stood the capitalist West, led by the United States, a federal republic with a two-party presidential system. The First World nations of the Western Bloc were generally liberal democratic with a free press and independent organizations, but were economically and politically entwined with a network of banana republics and other authoritarian regimes throughout the Third World, most of which were the Western Bloc's former colonies.[1][2] Some major Cold War frontlines such as Vietnam, Indonesia, and the Congo were still Western colonies in 1947.
# A small neutral bloc arose with the Non-Aligned Movement; it sought good relations with both sides. The two superpowers never engaged directly in full-scale armed combat, but they were heavily armed in preparation for a possible all-out nuclear world war. Each side had a nuclear strategy that discouraged an attack by the other side, on the basis that such an attack would lead to the total destruction of the attacker—the doctrine of mutually assured destruction (MAD). Aside from the development of the two sides' nuclear arsenals, and their deployment of conventional military forces, the struggle for dominance was expressed via proxy wars around the globe, psychological warfare, massive propaganda campaigns and espionage, rivalry at sports events, and technological competitions such as the Space Race.'''

stopset = set(stopwords.words('english'))
stopset.update(['.', ',', '"', "'", '?', '!', ':',
                ';', '(', ')', '[', ']', '{', '}'])

def relevance(sentence_, sentence):
	avg_len = len(sentence_) + len(sentence)
	avg_len /= 2.0
	return len(set(sentence) & set(sentence_)) / avg_len

def calculate_score(sentence, sentences):
	total_relevance_ = 0.0
	for sentence_ in sentences:
		relevance_ = relevance(sentence_, sentence)
		total_relevance_ += relevance_
	total_relevance_ /= len(sentences)
	return total_relevance_

def find_weak_sentences(corpus):
	tokenized_sentences = tokenize_sentences(corpus)
	scores = []
	for index, sentence in enumerate(tokenized_sentences):
		score = calculate_score(sentence, tokenized_sentences)
		scores.append((score, index))

# Tokenising all sentences 
def tokenize_sentences(sentences):
	sentence_tokenlize_list = sent_tokenize(sentences)
	# print "Number of sentences in the input text: " + str(len(sentence_tokenlize_list))
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
def bigram_finders(all_tokens):
	all_words = [token for tokens in all_tokens for token in tokens]
	all_words = list(set(all_words))
'''
Note:
Bigrams not really useful.
'''
def bigram_finders(query_tokens):
	important_words = [token for tokens in query_tokens for token in tokens]
	important_words = list(set(important_words))
	bigram_measures = nltk.collocations.BigramAssocMeasures()
	finder = BigramCollocationFinder.from_words(all_words)
	# print finder.nbest(bigram_measures.raw_freq, 10)


def term_frequency(corpus):
	# Term frequency.
	tf = []
	lower_corpus = corpus.lower()
	for word in important_words:
		count_ = lower_corpus.count(word)
		tf.append((word, count_))
	tf = sorted(tf, key=lambda x: x[1])
	#print tf

def get_possible_title(query_tokens):
	all_words = [token for tokens in query_tokens for token in tokens]
	nomod_words = []
	lemma = WordNetLemmatizer()
	stemmer = SnowballStemmer('english')
	for word in all_words:
		stemmed_word = str(stemmer.stem(word))
		lemmatized_word = str(lemma.lemmatize(word.lower()))
		nomod_words.append(lemmatized_word)
	freq_important_words = {}
	for word in nomod_words:
		count_ = nomod_words.count(word)
		if count_ in freq_important_words:
			freq_important_words[count_].append(word)
		else:
			freq_important_words[count_] = []
			freq_important_words[count_].append(word)
	most_freq_words = []
	max_count = -1
	for count in freq_important_words:
		if count > max_count:
			max_count = count
	count_ = max_count
	while max_count - count_ <= 1 and count_ > 0:
		for word in freq_important_words[count_]:
			most_freq_words.append(word)
		count_ -= 1
		while count_ not in freq_important_words and count_ > 0:
			count_ -= 1
	most_freq_words_ = ""
	for word in set(most_freq_words):
		most_freq_words_ += word + " "
	# print most_freq_words_
	return set(most_freq_words)

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
		return data, sentences
	except Exception as e:
	    print(e)


def fetch_search_queries(corpus):
	tokenized_sentences = tokenize_sentences(corpus)
	word_tokenized_sentences_ = word_tokenized_sentences(tokenized_sentences)
	bing_results, sentences = bing_text_analysis(tokenized_sentences)
	# print bing_results
	query_results = query_tokens(word_tokenized_sentences_)
	most_freq_words = get_possible_title(query_results)

	# print len(bing_results), len(query_results)
	ind_counter = 0
	search_queries = []
	bing_results = dict(bing_results)
	print bing_results
	lemma = WordNetLemmatizer()
	for results in bing_results['documents']:
		list_of_imp_words = query_results[ind_counter]
		ind_counter += 1
		imp_words = []
		for word in results['keyPhrases']:
			list_words = word.split(' ')
			words_count = 0
			for word_ in list_words:
				if str(word_) in list_of_imp_words:
					words_count += 1
			keep_word = False
			if words_count * 1.0 / len(list_words) >= 0.75:
				keep_word = True
			if keep_word:
				imp_words.append(str(word))
		search_query = ""
		most_freq_words_ = most_freq_words.copy()
		lemmatized_words = []
		for x in imp_words[ :MAX_STRINGS_IN_SEARCH_QUERY]:
			lemmatized_words.append(str(lemma.lemmatize(x.lower())))
		most_freq_words_.update(lemmatized_words)
		for word in set(most_freq_words_):
			search_query += word + " "
		search_queries.append(search_query)
	return search_queries, sentences

# find_weak_sentences(corpus)

# get_possible_title(query_tokens(word_tokenized_sentences(tokenize_sentences(corpus))))

# bigram_finders(word_tokenized_sentences(tokenize_sentences(corpus)))
# returns search queries and sentences used to create them. Use these sentences in TTS
search_queries, sentences = fetch_search_queries(corpus)
print search_queries
