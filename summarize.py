# coding=utf-8
import codecs
import nltk
import string
from nltk.corpus import stopwords
import re

stop_words = stopwords.words('english')

LOWER_BOUND = 0.20
UPPER_BOUND = 0.90

block_sep = '\n\n'


def unicode_(s):
	if type(s) == 'unicode':
		return s
	else:
		return codecs.unicode_escape_decode(s)[0]

def is_unimportant(word):
	return word in ['.', '!', ','] or '\'' in word or word in stop_words

def only_important(sent):
	return filter(lambda w: not is_unimportant(w), sent)

def compare_sents(sent1, sent2):
	if not len(sent1) or not len(sent2):
		return 0
	return len(set(only_important(sent1)) & set(only_important(sent2))) / ((len(sent1) + len(sent2)) / 2.0)

def compare_sents_bounded(sent1, sent2):
	cmpd = compare_sents(sent1, sent2)
	if LOWER_BOUND < cmpd < UPPER_BOUND:
		return cmpd
	else:
		return 0

def compute_score(sent, sents):
	if not len(sent):
		return 0
	sum_ = sum(compare_sents_bounded(sent, sent1) for sent1 in sents) / float(len(sents))
	return sum_

def summarize_block(block):
	if not block:
		return None
	sents = nltk.sent_tokenize(block)
	word_sents = list(map(nltk.word_tokenize, sents))
	d = dict((compute_score(word_sent, word_sents), sent) 
		for sent, word_sent in zip(sents, word_sents))
	return d[max(d.keys())]

def summarize_blocks(blocks):
	summaries = [re.sub('\s+', ' ', summarize_block(block) or '').strip()
	for block in blocks]
	summaries = sorted(set(summaries), key = summaries.index)
	return [unicode_(re.sub('\s+', ' ', summary.strip())) for summary in summaries if any(c.lower() in string.ascii_lowercase for c in summary)]

def summarize_text(text):
	return summarize_blocks(text.split(block_sep))

corpus = '''The Cold War was a state of geopolitical tension after World War II between powers in the Eastern Bloc (the Soviet Union and its satellite states) and powers in the Western Bloc (the United States, its NATO allies and others). Historians do not fully agree on the dates, but a common timeframe is the period between 1947, the year the Truman Doctrine, a U.S. foreign policy pledging to aid nations threatened by Soviet expansionism, was announced, and either 1989, when communism fell in Eastern Europe, or 1991, when the Soviet Union collapsed. The term "cold" is used because there was no large-scale fighting directly between the two sides, but they each supported major regional wars known as proxy wars.

The Cold War split the temporary wartime alliance against Nazi Germany, leaving the Soviet Union and the United States as two superpowers with profound economic and political differences. The USSR was a Marxist–Leninist state led by its Communist Party, which in turn was dominated by a leader with different titles over time, and a small committee called the Politburo. The Party controlled the press, the military, the economy and many organizations. It also controlled the other states in the Eastern Bloc, and funded Communist parties around the world, sometimes in competition with Communist China, particularly following the Sino-Soviet split of the 1960s. In opposition stood the capitalist West, led by the United States, a federal republic with a two-party presidential system. The First World nations of the Western Bloc were generally liberal democratic with a free press and independent organizations, but were economically and politically entwined with a network of banana republics and other authoritarian regimes throughout the Third World, most of which were the Western Bloc's former colonies.[1][2] Some major Cold War frontlines such as Vietnam, Indonesia, and the Congo were still Western colonies in 1947.

A small neutral bloc arose with the Non-Aligned Movement; it sought good relations with both sides. The two superpowers never engaged directly in full-scale armed combat, but they were heavily armed in preparation for a possible all-out nuclear world war. Each side had a nuclear strategy that discouraged an attack by the other side, on the basis that such an attack would lead to the total destruction of the attacker—the doctrine of mutually assured destruction (MAD). Aside from the development of the two sides' nuclear arsenals, and their deployment of conventional military forces, the struggle for dominance was expressed via proxy wars around the globe, psychological warfare, massive propaganda campaigns and espionage, rivalry at sports events, and technological competitions such as the Space Race.'''

summary = summarize_text(corpus)
for summary_ in summary:
	print(summary_)