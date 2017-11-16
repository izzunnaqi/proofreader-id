#!/usr/bin/env python -W ignore::DeprecationWarning
# -*- coding: utf-8 -*-qq

import sys
import re
import xml.etree.ElementTree as et
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk import sent_tokenize
from random import randint
from Levenshtein import distance

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
						# item = re.sub('<segment>', '<segment>\n\t', item)
						# item = re.sub('</segment>', '\n</segment>', item)
						res = res + item



	res = res + "\n</document>"

	res = re.sub("</segment><segment>", "", res)
	res = res.encode('utf-8')
	
	return res


def align(arg1, arg2):
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
		partial_match, not_match = partial(not_match, 10, 5)
		
	return full_match, partial_match, not_match


def partial(x, k, t):
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

def label(x):
	result = ""

	m = 1
	for a, b in x:
		sent_a = sent_tokenize(a)
		sent_b = sent_tokenize(b)

		print "==========="
		print "Segment " + str(m)
		print "==========="
		
		sentences = sent_align(sent_a, sent_b)
		m += 1


	return result


def sent_align(sentlist_a, sentlist_b):
	match = []
	not_match = []
	indexes = []
	partial = []

	i = 0
	j = 0
	m = len(sentlist_a)
	n = len(sentlist_b)
	
	while (i < m and j < n):
		
		# full match
		regex_1 = re.compile('(.*)%s(.*)'%re.escape(sentlist_a[i]), re.IGNORECASE)
		regex_2 = re.compile('(.*)%s(.*)'%re.escape(sentlist_b[j]), re.IGNORECASE)
		
		if i != (m-1) and j != (n-1):
			if len(sentlist_a[i]) > 15 and len(sentlist_b[j]) > 15 and len(sentlist_a[i+1]) > 15 and len(sentlist_b[j+1]) > 15:

				if regex_1.match(sentlist_b[j]):
					match.append([sentlist_a[i], sentlist_b[j]])
					
				elif regex_2.match(sentlist_a[i+1]):  
					match.append([sentlist_a[i+1], sentlist_b[j]])
					
					if distance(sentlist_a[i], sentlist_b[j]) < 65:
						partial.append([sentlist_a[i], sentlist_b[j]])
					else:
						not_match.append([sentlist_a[i], sentlist_b[j]])

				elif regex_1.match(sentlist_b[j+1]):
					match.append([sentlist_a[i], sentlist_b[j+1]])
					
					if distance(sentlist_a[i], sentlist_b[j]) < 65:
						partial.append([sentlist_a[i], sentlist_b[j]])
					else:
						not_match.append([sentlist_a[i], sentlist_b[j]])

				else:
					indexes.append([i,j])
					
					if distance(sentlist_a[i], sentlist_b[j]) < 65:
						partial.append([sentlist_a[i], sentlist_b[j]])
					else:
						not_match.append([sentlist_a[i], sentlist_b[j]])
					
					if distance(sentlist_a[i+1], sentlist_b[j]) < 65:
						partial.append([sentlist_a[i+1], sentlist_b[j]])
					else:
						not_match.append([sentlist_a[i+1], sentlist_b[j]])
					
					if distance(sentlist_a[i], sentlist_b[j+1]) < 65:
						partial.append([sentlist_a[i], sentlist_b[j+1]])
					else:
						not_match.append([sentlist_a[i+1], sentlist_b[j]])
		else:
			if len(sentlist_a[i]) > 15 and len(sentlist_b[j]) > 15:			
				if regex_1.match(sentlist_b[j]):
					match.append([sentlist_a[i], sentlist_b[j]])

				else:
					indexes.append([i,j])
					if distance(sentlist_a[i], sentlist_b[j]) < 65:
						partial.append([sentlist_a[i], sentlist_b[j]])
					else:
						not_match.append([sentlist_a[i], sentlist_b[j]])

		i += 1
		j += 1	

	print "Full Match"
	for a, b in match:
		print "Distance: " + str(distance(a, b))
		print "Before: " + a
		print "After: " + b
		print ""

	print "--------------\n"
	print "Partial"
	for a, b in partial:
		print "Distance: " + str(distance(a, b))
		print "Before: " + a
		print "After: " + b
		print ""

	print ""
	return match


def word_align(wordlist_1, wordlist_2):
	pair_candidate = []

	return pair_candidate


def italic(token_a, token_b):
	result = ""
	before_tag = "<BEFORE>"
	c_before_tag = "</BEFORE>"
	after_tag = "<AFTER>"
	c_after_tag = "</AFTER>"

	
	return result


def main():
	config()
	
	doc1 = sys.argv[1]
	doc2 = sys.argv[2]

	xml_1 = simplify(doc1)
	xml_2 = simplify(doc2)
	
	full, partial, not_match = align(xml_1, xml_2)

	a = label(partial)


if __name__ == '__main__':
	main()
