#!/usr/bin/env python -W ignore::DeprecationWarning
# -*- coding: utf-8 -*-qq

import sys
import re
import xml.etree.ElementTree as et
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk import sent_tokenize
from random import randint

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
	match = []
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
				match.append([str1, str2])
			else:
				not_match.append([str1, str2])


	if len(not_match) > 0:
		a = partial(not_match, 10, 5)
		for m, n in a:
			match.append([m, n])

	return match		


def partial(x, k, t):

	match = []

	for a, b in x:
		token_a = word_tokenize(a)
		token_b = word_tokenize(b)

		for i in xrange(0, k):
			m = 0
			
			if len(token_a) - t > 0:
				m = randint(0, len(token_a) - t)

			rand_a = " ".join(token_a[m:m+t])
			
			if rand_a in b:
				match.append([a, b])
				break

	return match



def label(x):
	result = ""

	for a, b in x:
		sent_a = sent_tokenize(a)
		sent_b = sent_tokenize(b)

		sentences = sent_align(sent_a, sent_b)
		
		# print sentences
		for i, j in sentences:
			print i
			print "--------"
			print j
			print 

			token_a = word_tokenize(i)
			token_b = word_tokenize(j)

			result = result + italic(token_a, token_b)

	return result


def sent_align(sentlist_a, sentlist_b):
	match = []

	for a in sentlist_a:
		for b in sentlist_b:

			# full match
			regex_1 = re.compile('(.*)%s(.*)'%re.escape(a), re.IGNORECASE)
			regex_2 = re.compile('(.*)%s(.*)'%re.escape(b), re.IGNORECASE)

			if regex_1.match(b):
				match.append([a, b])

			elif regex_2.match(a):
				match.append([a, b])
			
			else:
				pair = [[a, b]]

				part = partial(pair, 5, 3)

				for m, n in part:
					match.append([m,n])

	return match


def italic(token_a, token_b):
	result = ""
	before_tag = "<BEFORE>"
	c_before_tag = "</BEFORE>"
	after_tag = "<AFTER>"
	c_after_tag = "</AFTER>"

	for i in xrange(0, len(token_a)):
			
			for j in xrange(0, len(token_b)):

				tag_i = "".join(token_a[i-3:i])
				ctag_i = "".join(token_a[i+1:i+4])

				tag_j = "".join(token_b[j-3:j])
				ctag_j = "".join(token_b[j+1:j+4])

				if token_a[i] == token_b[j]:
					
					if tag_i == "<it>" and tag_j !="<it>":
						result = result + before_tag + tag_i + token_a[i] + ctag_i + c_before_tag + "\n" + after_tag + token_b[j] + c_after_tag +  "\n\n"
						

					elif (tag_j == "<it>" and tag_i != "<it>"):
						result = result + before_tag + token_a[i] + c_before_tag + "\n" + after_tag + tag_j + token_b[j] + ctag_j + c_after_tag + "\n\n"

	return result


def main():
	config()
	
	doc1 = sys.argv[1]
	doc2 = sys.argv[2]

	xml_1 = simplify(doc1)
	xml_2 = simplify(doc2)
	
	result = align(xml_1, xml_2)

	lbl = label(result)

	print lbl
	# for i in result:
	#  	print i[0] + "\n===||===\n" + i[1]
	#  	print "~~~~~~~~~~~~~~~~~~~~~~~~~"


if __name__ == '__main__':
	main()
