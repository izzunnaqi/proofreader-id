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
	allpage = pages.findall("page")

	temp = "<?xml version=\"1.0\" encoding=\"utf-8\" ?>\n<document>\n"
	
	# read page
	for p in allpage:
		page_str = ""

		# read line
		for el in p.findall("textbox"):
			line = ""
			flag_it = 0
			flag_bo = 0

			for t in el.findall("textline/text"):
				if t.text is None:
					
					if flag_bo == 1:
						line = line + "</bo>"
						flag_bo = 0

					if flag_it == 1:
						line = line + "</it>"
						flag_it = 0
					
					if line is not "" and line[-1] is " ":
						line = line	
					else:
						line = line + " "
				else:
					if t.text == '&':
						line = line + '&amp;'
					elif t.text == '>':
						line = line + "&gt;"
					elif t.text == '<':
						line = line + "&lt;"
					else:
						if "Italic" in t.attrib['font'] and flag_it == 0:
							flag_it = 1

							if line is "" or not line[-1].isalpha():
								line = line + "<it>"
						
						if "Bold" in t.attrib['font'] and flag_bo == 0:
							flag_bo = 1

							if line is "" or not line[-1].isalpha():
								line = line + "<bo>"

						line = line + t.text

			# temp = temp + '\n'
			# sentences = tokenize.sent_tokenize(line)
			# for i in range(0, len(sentences)):
			if line is not " ":
				# page_str = page_str +  "<sentence>" +sentences[i]+"</sentence>\n"
				if line[-1] is " ":
					page_str = page_str +  "<line>" +line[0:-1]+"</line>\n"	
				else:
					page_str = page_str +  "<line>" +line+"</line>\n"
	
		
		page_num = re.findall('<line>[0-9]+</line>', page_str)
		page_tag = ""
		
		if len(page_num) > 0:
			page_tag = '<page id=\"'+ p.attrib['id']+'\" class=\"isi\">\n'
		else:
			page_tag = '<page id=\"'+ p.attrib['id']+'\" class=\"awal\">\n'
		
		temp = temp + page_tag + page_str + '</page>\n'


	temp = temp + "</document>"
	temp = temp.encode("utf-8")

	return temp

def main():
	config()
	a = extract_xml(sys.argv)
	
	print a


if __name__ == '__main__':
	main()