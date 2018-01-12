#!/usr/bin/env python -W ignore::DeprecationWarning
# -*- coding: utf-8 -*-qq

import sys
import re
import optparse
import re, math
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk import sent_tokenize
from random import randint
from Levenshtein import distance
from collections import Counter

WORD = re.compile(r'\w+')

def config():
	reload(sys)
	sys.setdefaultencoding('utf-8')


def simplify(xmldoc):
	res = "<?xml version=\"1.0\" encoding=\"utf-8\" ?>\n<document>"

	with open(xmldoc) as fp:
		soup = BeautifulSoup(fp, 'lxml')

	pages = soup.find_all('page')

	for p in pages:

		if p.pagenum is not None:
			a = unicode(p.pagenum.string)
			a = str(a)

			if a.isdigit() and len(a) < 4:
				for item in p.contents:
					if item.name != "pagenum" and item.name != "footer" and item.name is not None:
						item = str(item)
						item = re.sub('\t|\n', "", item)
						res = res + item



	res = res + "\n</document>"

	res = re.sub("</segment><segment>", "", res)
	res = res.encode('utf-8')
	
	return res


def segment_align(arg1, arg2):
	full_match = []
	partial_match = []
	not_match = []
	
	soup1 = BeautifulSoup(arg1, 'xml').document
	soup2 = BeautifulSoup(arg2, 'xml').document

	doc1 = soup1.contents
	doc2 = soup2.contents

	title_1 = soup1.find_all('title')
	title_2 = soup2.find_all('title')

	indexes = []

	for a in title_1:
		for b in title_2:
			if a == b:
				indexes.append([doc1.index(a), doc2.index(b)])

	for i in indexes:
		x = doc1[i[0]+1]
		y = doc2[i[1]+1]

		if x.name == "segment" and y.name == "segment":
			str1 = "".join(str(e) for e in x.contents)
			str2 = "".join(str(e) for e in y.contents)

			# full match
			regex = re.compile('(.*)%s(.*)'%re.escape(str1), re.IGNORECASE)
			
			if regex.match(str2):
				full_match.append([str1, str2])
			else:
				not_match.append([str1, str2])


	if len(not_match) > 0:
		partial_match, not_match = partial_segment(not_match, 10, 5)
		
	return full_match, partial_match, not_match


def partial_segment(x, k, t):
	match = []
	not_match = x
	
	for a, b in not_match:
		token_a = word_tokenize(a)
		token_b = word_tokenize(b)

		for i in xrange(0, k):
			m = 0
			
			if len(token_a) - t > 0:
				m = randint(0, len(token_a) - t)

			rand_a = " ".join(token_a[m:m+t])
			
			if rand_a in b:
				not_match.remove([a, b])

				match.append([a, b])
				break

	return match, not_match


def sentence_align(sentlist_a, sentlist_b):
	match = []
	not_match = []
	partial = []

	sentlist_a = trim_double_space(sentlist_a)
	sentlist_b = trim_double_space(sentlist_b)

	i = 0
	j = 0
	m = len(sentlist_a)
	n = len(sentlist_b)
	
	while (i < m and j < n):
		regex_1 = re.compile('(.*)%s(.*)'%re.escape(sentlist_a[i]), re.IGNORECASE)
		regex_2 = re.compile('(.*)%s(.*)'%re.escape(sentlist_b[j]), re.IGNORECASE)
		
		if i != (m-1) and j != (n-1):
			if len(sentlist_a[i]) > 15 and len(sentlist_b[j]) > 15 and len(sentlist_a[i+1]) > 15 and len(sentlist_b[j+1]) > 15:

				if regex_1.match(sentlist_b[j]):
					match.append([sentlist_a[i], sentlist_b[j]])
					
				elif regex_2.match(sentlist_a[i+1]):  
					match.append([sentlist_a[i+1], sentlist_b[j]])

				elif regex_1.match(sentlist_b[j+1]):
					match.append([sentlist_a[i], sentlist_b[j+1]])

				else:
					if partial_sentence(sentlist_a[i], sentlist_b[j]):
						partial.append([sentlist_a[i], sentlist_b[j]])
					
					elif partial_sentence(sentlist_a[i+1], sentlist_b[j]):
						partial.append([sentlist_a[i+1], sentlist_b[j]])
					
					elif partial_sentence(sentlist_a[i], sentlist_b[j+1]):
						partial.append([sentlist_a[i], sentlist_b[j+1]])

		else:
			if len(sentlist_a[i]) > 15 and len(sentlist_b[j]) > 15:			
				if regex_1.match(sentlist_b[j]):
					match.append([sentlist_a[i], sentlist_b[j]])
				else:
					if partial_sentence(sentlist_a[i], sentlist_b[j]):
						partial.append([sentlist_a[i], sentlist_b[j]])

		i += 1
		j += 1	

	
	return match, partial

def trim_double_space(sentence_list):
	res = []
	for i in sentence_list:
		a = i.replace("  ", " ")
		res.append(a)

	return res

def jaccard_similarity(query, document):
    intersection = set(query).intersection(set(document))
    union = set(query).union(set(document))

    return float(float(len(intersection)) / float(len(union)))

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)

def partial_sentence(text1, text2):
	query = text1.split(" ")
	document = text2.split(" ")

	jacc = jaccard_similarity(query, document)

	if jacc > 0.3:
		return True
	else:
		return False


def main():
	config()
	
	doc1 = sys.argv[1]
	doc2 = sys.argv[2]

	xml_1 = simplify(doc1)
	xml_2 = simplify(doc2)
	
	full, partial_seg, not_match = segment_align(xml_1, xml_2)

	candidate = []
	res = ""
	count_pair = 0
	for a, b in partial_seg:

		sent_a = sent_tokenize(a)
		sent_b = sent_tokenize(b)

		full_sent, partial_sent = sentence_align(sent_a, sent_b)
		count_pair += len(partial_sent)
		
		for x, y in partial_sent:
			res += "<PAIR>\n"
			res += "<BEFORE>" + x + "</BEFORE>\n"
			res += "<AFTER>" + y + "</AFTER>\n"
			res += "<ERRTYPE></ERRTYPE>\n"
			res += "</PAIR>\n\n"


	parser = optparse.OptionParser()
	parser.add_option('-o', action="store")

	options, args = parser.parse_args()

	with open(options.o, 'a') as f:
		f.write(res)

	print 'Pair collected: ', str(count_pair)


if __name__ == '__main__':
	main()
