#!/usr/bin/env python -W ignore::DeprecationWarning
# -*- coding: utf-8 -*-qq

import sys
import re
import xml.etree.ElementTree as et
from bs4 import BeautifulSoup

def config():
	reload(sys)
	sys.setdefaultencoding('utf-8')


def align(arg1, arg2):
	match = []
	error_candidate = []
	
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
		if doc1[i[0]+1].name == "segment" and doc2[i[1]+1].name == "segment":
			match.append([doc1[i[0]+1], doc2[i[1]+1]])


	
	return match		
		



def simplify(xmldoc):
	res = "<?xml version=\"1.0\" encoding=\"utf-8\" ?>\n<document>"

	with open(xmldoc) as fp:
		soup = BeautifulSoup(fp, 'lxml')

	pages = soup.find_all('page')

	for p in pages:

		if p.pagenum.string is not None:
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


	# print xml_1
	
	result = align(xml_1, xml_2)

	for a in result:
		print str(a[0]) + "\n===||===\n" + str(a[1])
		print "~~~~~~~~~~~~~~~~~~~~~~~~~"


if __name__ == '__main__':
	main()
