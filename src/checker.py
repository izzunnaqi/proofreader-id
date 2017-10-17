 #!/usr/bin/env python
## -*- coding: utf-8 -*-qq

import sys
import re
import xml.etree.ElementTree as et
import nltk

from polyglot.text import Text

def config():
	reload(sys)
	sys.setdefaultencoding('utf-8')

def space_on_punctuation(pages):
	pass

def check_dots(pages):
	row = ""
	mistakes = ""

	for i in range(0, len(pages)):

		# rule untuk false positif, kesalahan penggunaan spasi
		if len(re.findall('[a-zA-Z]+\.[a-zA-Z]+', pages[i])) > 0:
			if len(re.findall('(http[s]?://|www.)[^"\' ]+', pages[i])) > 0:
				row = row;
			elif len(re.findall('\s[A-Z]{1,2}\.[a-zA-Z]{1,3}\.[a-zA-Z]{0,3}\.?', pages[i])) > 0:
				row = row;
			else:
				row = row + str(i+1) + ", "
				mistakes = mistakes + ('\n').join(re.findall('[a-zA-Z]+\.[a-zA-Z]+', pages[i]))

		if len(re.findall('[1-9]\.[1-9]\.[a-zA-Z]+', pages[i])) > 0:
			row = row + str(i+1) + ", "
			mistakes = mistakes + ('\n').join(re.findall('[1-9]\.[1-9]\.[a-zA-Z]+', pages[i]))

		if len(re.findall('[1-9]\.[1-9]\.[1-9]\.[a-zA-Z]+', pages[i])) > 0:
			row = row + str(i+1) + ", "
			print re.findall('[1-9]\.[1-9]\.[1-9]\.[a-zA-Z]+', pages[i])

		if len(re.findall('(.*)[1-9]+\.\s[0-9][a-zA-Z]*', pages[i])) > 0:
			row = row + str(i+1) + ", "
			print re.findall('(.*)[1-9]+\.\s[0-9][a-zA-Z]*', pages[i])
	
	if len(row) < 1:
		row = ""
	else:
		row = "kalimat " + row[0:-2]

	return mistakes

def check_comma(pages):
	row = ""

	for i in range(0, len(pages)):
		if len(re.findall('[a-zA-Z]+\,[a-zA-Z]+', pages[i])) > 0:
			row = row + str(i+1) + ", "
			print re.findall('[a-zA-Z]+\,[a-zA-Z]+', pages[i])

		if len(re.findall('dan\,', pages[i])) > 0:
			row = row + str(i+1) + ", "
			print re.findall('dan\,', pages[i])

	if len(row) < 1:
		row = ""
	else:
		row = "kalimat " + row[0:-2]

	return row	

def check_semicolon(pages):
	row = ""

	for i in range(0, len(pages)):
		if len(re.findall('[a-zA-Z]+\;[a-zA-Z]+', pages[i])) > 0:
			row = row + str(i+1) + ", "
			print re.findall('[a-zA-Z]+\;[a-zA-Z]+', pages[i])

	if len(row) < 1:
		row = ""
	else:
		row = "kalimat " + row[0:-2]

	return row	

def check_colon(pages):
	row = ""

	for i in range(0, len(pages)):
		if len(re.findall('[a-zA-Z]+\:[a-zA-Z]+', pages[i])) > 0:
			row = row + str(i+1) + ", "
			print re.findall('[a-zA-Z]+\:[a-zA-Z]+', pages[i])

	if len(row) < 1:
		row = ""
	else:
		row = "kalimat " + row[0:-2]

	return row	

def check_bracket(pages):
	pass

def main():
	config()
	in_file = sys.argv[1]

	tree = et.parse(in_file)
	root = tree.getroot()
	pages = root.findall('page')

	
	for page in pages:
		
		if page.attrib['class'] == 'isi':
			lines = page.findall('line')
			temp = []
				
			for s in lines:			
				
				line = ""
				for i in s.itertext():
					line = line + i
				
				text = Text(line, hint_language_code='id')

				for entity in text.entities:
					if entity.tag == 'I-PER':
						
						print str(entity)

				temp.append(line)
	
		
		# dots = check_dots(temp)
		# if len(dots) > 0:
		# 	print "kesalahan titik pada halaman "+ e.attrib['id'] +"\n"+dots

		# comma = check_comma(temp)
		# if len(comma) > 0:
		# 	print "kesalahan koma pada halaman "+ e.attrib['id'] +" "+comma

		# semicolon = check_semicolon(temp)
		# if len(semicolon) > 0:
		# 	print "kesalahan titik koma pada halaman "+ e.attrib['id'] +" "+semicolon

		# colon = check_colon(temp)
		# if len(colon) > 0:
		# 	print "kesalahan titik dua pada halaman "+ e.attrib['id'] +" "+colon
	

if __name__ == '__main__':
	main()