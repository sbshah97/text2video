# coding=utf-8

from imports import *
from summarize import summarize_text
from nltk.corpus import wordnet as wn
from textblob import TextBlob

import re

sentence_re = r'(?:(?:[A-Z])(?:.[A-Z])+.?)|(?:\w+(?:-\w+)*)|(?:\$?\d+(?:.\d+)?%?)|(?:...|)(?:[][.,;"\'?():-_`])'
lemmatizer = WordNetLemmatizer()
stemmer = nltk.stem.porter.PorterStemmer()
stopwords = stopwords.words('english')

def leaves(tree):
	for subtree in tree.subtrees(filter = lambda t: t.label() == 'NP'):
		yield subtree.leaves()

def normalize(word):
	word = word.lower().encode('utf-8')
	word = str(unicode(word, 'ascii', 'ignore'))
	word = lemmatizer.lemmatize(word)
	return word

def get_similar_words(word):
	synsets = wn.synsets(word, pos='n')
	if len(synsets) == 0:
		return []
	else:
		synset = synsets[0]
	hypernym = synset.hypernyms()[0]
	hyponyms = hypernym.hyponyms()

	similar_words = []
	for hyponym in hyponyms:
		similar_word = hyponym.lemmas()[0].name().replace('_', ' ')
		if similar_word != word:
			similar_words.append(str(similar_word))
		if len(similar_words) == 6:
			break
	return similar_words

def acceptable_word(word):
	accepted = bool(2 <= len(word) <= 40 and word.lower() not in stopwords)
	return accepted

def get_terms(tree):
	for leaf in leaves(tree):
		term = [normalize(w) for w, t in leaf if acceptable_word(w)]
		yield term

def set_noun_phrases(tree, corpus):
	noun_phrases = []
	terms = get_terms(tree)
	for term in terms:
		for word in term:
			noun_phrases.append(word)
	return noun_phrases

def get_questionnaire(tokens_tags, tree, sentence):
	noun_phrases = set_noun_phrases(tree, sentence)
	replace_nouns = []
	for word, tag in tokens_tags:
		if tag == 'NN':
			for phrase in noun_phrases:
				if word in phrase:
					[replace_nouns.append(phrase_word) for phrase_word in phrase.split()[-2: ]]
					break
			if len(replace_nouns) == 0:
				print word
				replace_nouns.append(word)
			break
	if len(replace_nouns) == 0:
		return None

	questionnaire_ = {
		'answer': ' '.join(replace_nouns)
	}
	if len(replace_nouns) == 1:
		questionnaire_['similar_words'] = get_similar_words(replace_nouns[0])
	else:
		questionnaire_['similar_words'] = []
	replace_phrase = ' '.join(replace_nouns)
	blanks_phrase = ('__' * len(replace_nouns)).strip()
	expression = re.compile(re.escape(replace_phrase), re.IGNORECASE)
	sentence = expression.sub(blanks_phrase, str(sentence), count=1)
	questionnaire_['question'] = sentence
	return questionnaire_


def get_questions(corpus):
	grammer = r"""
		NBAR: 
			{<NN.*|JJ>*<NN.*>}
		NP:
			{<NBAR>}
			{<NBAR><IN><NBAR>}
	"""
	summary = summarize_text(corpus)
	trivia = []
	for summary_ in summary:
		chunker = nltk.RegexpParser(grammer)
		toks = nltk.regexp_tokenize(summary_, sentence_re)
		postoks = nltk.tag.pos_tag(toks)
		tree = chunker.parse(postoks)
		questionnaire_ = get_questionnaire(postoks, tree, summary_)
		trivia.append(questionnaire_)
	return trivia

corpus = '''The Cold War was a state of geopolitical tension after World War II between powers in the Eastern Bloc (the Soviet Union and its satellite states) and powers in the Western Bloc (the United States, its NATO allies and others). Historians do not fully agree on the dates, but a common timeframe is the period between 1947, the year the Truman Doctrine, a U.S. foreign policy pledging to aid nations threatened by Soviet expansionism, was announced, and either 1989, when communism fell in Eastern Europe, or 1991, when the Soviet Union collapsed. The term "cold" is used because there was no large-scale fighting directly between the two sides, but they each supported major regional wars known as proxy wars.
The Cold War split the temporary wartime alliance against Nazi Germany, leaving the Soviet Union and the United States as two superpowers with profound economic and political differences. The USSR was a Marxist–Leninist state led by its Communist Party, which in turn was dominated by a leader with different titles over time, and a small committee called the Politburo. The Party controlled the press, the military, the economy and many organizations. It also controlled the other states in the Eastern Bloc, and funded Communist parties around the world, sometimes in competition with Communist China, particularly following the Sino-Soviet split of the 1960s. In opposition stood the capitalist West, led by the United States, a federal republic with a two-party presidential system. The First World nations of the Western Bloc were generally liberal democratic with a free press and independent organizations, but were economically and politically entwined with a network of banana republics and other authoritarian regimes throughout the Third World, most of which were the Western Bloc's former colonies.[1][2] Some major Cold War frontlines such as Vietnam, Indonesia, and the Congo were still Western colonies in 1947.
A small neutral bloc arose with the Non-Aligned Movement; it sought good relations with both sides. The two superpowers never engaged directly in full-scale armed combat, but they were heavily armed in preparation for a possible all-out nuclear world war. Each side had a nuclear strategy that discouraged an attack by the other side, on the basis that such an attack would lead to the total destruction of the attacker-the doctrine of mutually assured destruction (MAD). Aside from the development of the two sides' nuclear arsenals, and their deployment of conventional military forces, the struggle for dominance was expressed via proxy wars around the globe, psychological warfare, massive propaganda campaigns and espionage, rivalry at sports events, and technological competitions such as the Space Race.'''

trivia = get_questions(corpus)
for trivia_ in trivia:
	print trivia_