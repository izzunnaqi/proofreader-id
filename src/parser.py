#!/usr/bin/env python -W ignore::DeprecationWarning
# -*- coding: utf-8 -*-qq

import sys
import re
import xml.etree.ElementTree as et

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
		lines = []

		# read line
		for el in p.findall("textbox"):
			line = ""
			flag_it = 0
			flag_bo = 0

			for t in el.findall("textline/text"):
				
				if t.text.isspace() or t.text is None:
					
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

			
			if line is not " ":
				# if line[-1] is " ":
				# 	lines.append(line[0:-1]);
				# else:
				# 	lines.append(line)
				lines.append(line)
		
		
		par = ""
		flag_par = 0
		
		for item in lines:
			
			if not item.isspace():
				if re.match('[<>a-zA-Z]+\.{0,1}', item) is not None:
					if flag_par == 0:
						par = par + "\n\t\t<par>\n\t\t\t" + item
						flag_par = 1	
					else:
						par = par + item
				else:
					if flag_par == 1:
						flag_par = 0
						par = par + "\n\t\t</par>\n\t\t" + item
					else:
						par = par + item
			else:
				par = par + item
		

		page_tag = '\t<page id=\"'+ p.attrib['id']+'\">\n\t\t'
		if flag_par == 1:
			temp = temp + page_tag + par + "\n\t\t</par>" + '\n\t</page>\n'
		else:
			temp = temp + page_tag + par + '\n\t</page>\n'

	temp = temp + "\n</document>"
	temp = temp.encode("utf-8")

	return temp

def main():
	config()
	a = extract_xml(sys.argv)
	
	print a

if __name__ == '__main__':
	main()