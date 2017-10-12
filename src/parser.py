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
				lines.append(line)
		
		
		segment = ""
		flag_seg = 1 
		
		for item in lines:
			if not item.isspace():
				trim = re.sub('<bo>|</bo>|<it>|</it>', '', item)

				if re.match('[0-9]+\.+[0-9]+\.+[0-9]*\.*\s+', trim) is not None or (trim.isupper() and "." not in trim) :
					if flag_seg == 0:
						segment = segment + "\n\t\t</segment>" + "\n\t\t<title>" + item + "</title>"
						flag_seg = 1
					else:
						segment = segment + "\n\t\t<title>" + item + "</title>"
						flag_seg = 1
				elif "Universitas Indonesia" in trim:
					
					if flag_seg == 0:
						segment = segment + "\n\t\t</segment>" + "\n\t\t<footer>" + item + "</footer>"
						flag_seg = 1
					else:
						segment = segment + "\n\t\t<footer>" + item + "</footer>"
						flag_seg = 1
				
				elif (trim.strip().isdigit() and len(trim.strip()) <= 4) or (re.match(r'\b[vix]+\b(?![,])', trim) is not None and len(trim.strip()) <= 4):
					if flag_seg == 0:
						segment = segment + "\n\t\t</segment>" + "\n\t\t<pagenum>" + item + "</pagenum>"
						flag_seg = 1
					else:
						segment = segment + "\n\t\t<pagenum>" + item + "</pagenum>"
						flag_seg = 1
				else:
					if flag_seg == 1:
						segment = segment + "\n\t\t<segment>\n\t\t\t" + item
						flag_seg = 0
					else:
						segment = segment + item
		

		page_tag = '\t<page id=\"'+ p.attrib['id']+'\">'
		
		if flag_seg == 0:
			temp = temp + page_tag + segment + "\n\t\t</segment>" + '\n\t</page>\n'
		else:
			temp = temp + page_tag + segment + '\n\t</page>\n'

	temp = temp + "\n</document>"
	temp = temp.encode("utf-8")

	return temp

def main():
	config()
	a = extract_xml(sys.argv)
	
	print a

if __name__ == '__main__':
	main()