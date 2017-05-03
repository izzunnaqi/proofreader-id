#!/usr/bin/env python -W ignore::DeprecationWarning
# -*- coding: utf-8 -*-qq

import sys
import re
import xml.etree.ElementTree as et
from nltk import tokenize

def config():
	reload(sys)
	sys.setdefaultencoding('utf-8')


def extract_xml(argv):
	in_file = sys.argv[1]

	tree = et.parse(in_file)
	pages = tree.getroot()
	page = pages.find("page")
	allpage = pages.findall("page")

	temp = ''
	pages = {}
	textbox = page.findall("textbox")

	temp = "<?xml version=\"1.0\" encoding=\"utf-8\" ?>\n<document>\n"
	
	# read page
	for p in allpage:
		temp = temp + '<page id=\"'+ p.attrib['id']+'\">\n'
		page_str = ""

		# read line
		for el in p.findall("textbox"):
			line = ""
			
			for t in el.findall("textline/text"):
				if 'bbox' in t.attrib:
					if t.text is None:
						# temp = temp + " "
						line = line + " "
					else:
						if t.text == '&':
							# temp = temp + '&amp;'
							line = line + '&amp;'
						elif t.text == '>':
							# temp = temp + "&gt;"
							line = line + "&gt;"
						elif t.text == '<':
							# temp = temp + "&lt;"
							line = line + "&lt;"
						else:
							# temp = temp + t.text
							line = line + t.text

			# temp = temp + '\n'
			page_str = page_str + line
			# sentences = tokenize.sent_tokenize(line)
			# for i in range(0, len(sentences)):
			# 	print "<sentence id=\"" + str(i) +"\">" +sentences[i]+"</sentence>"
		
	
		sentences = tokenize.sent_tokenize(page_str)
		page_str = ""
		for i in range(0, len(sentences)):
			page_str = page_str + "<sentence id=\"" + str(i+1) +"\">" +sentences[i]+"</sentence>\n"
			
		temp = temp + page_str + '</page>\n'

		num = int(p.attrib['id'])
		pages[num] = temp.splitlines()
		# temp = ''

	temp = temp + "</document>"
	temp = temp.encode("utf-8")

	return temp

def main():
	config()
	a = extract_xml(sys.argv)
	
	print a


if __name__ == '__main__':
	main()