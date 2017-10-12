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

	doc1 = BeautifulSoup(arg1, 'lxml')
	doc2 = BeautifulSoup(arg2, 'lxml')

	title_1 = doc1.find_all('title')
	title_2 = doc2.find_all('title')


	for i in title_1:
		i = [str(a) for a in i.contents]
		i = "".join(i)

		for j in title_2:
			j = [str(a) for a in j.contents]
			j = "".join(j)				

			if i[:-1] == j[:-1]:
				match.append([i, j])
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

			if a.strip().isdigit():
				for item in p.contents:
					if item.name != "pagenum" and item.name != "footer" and item.name is not None:
						item = str(item)
						item = re.sub('\t|\n', "", item)
						item = re.sub('<segment>', '<segment>\n\t', item)
						item = re.sub('</segment>', '\n</segment>', item)
						res = res + '\n' + item



	res = res + "\n</document>"
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
		print i


if __name__ == '__main__':
	main()
