#!/usr/bin/env python -W ignore::DeprecationWarning
# -*- coding: utf-8 -*-qq

import sys
import re
import xml.etree.ElementTree as et
from bs4 import BeautifulSoup
from nltk import word_tokenize
from random import randint

def config():
	reload(sys)
	sys.setdefaultencoding('utf-8')


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
		a = partial(not_match)
		for m, n in a:
			match.append([m, n])

	return match		


def partial(x):
	match = []

	for a, b in x:
		token_a = word_tokenize(a)
		token_b = word_tokenize(b)

		for i in xrange(0, 5):
			m = randint(0, len(token_a) - 7)
			# n = randint(0, len(token_b) - 3)

			rand_a = " ".join(token_a[m:m+7])
			
			if rand_a in b:
				match.append([a, b])
				break

	return match

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

def main():
	config()
	
	doc1 = sys.argv[1]
	doc2 = sys.argv[2]

	xml_1 = simplify(doc1)
	xml_2 = simplify(doc2)
	
	result = align(xml_1, xml_2)

	for i in result:
	 	print i[0] + "\n===||===\n" + i[1]
	 	print "~~~~~~~~~~~~~~~~~~~~~~~~~"


if __name__ == '__main__':
	main()
