#!/usr/bin/env python
import sys
import re
import xml.etree.ElementTree as et
import nltk

def check_dots(pages):
	row = ""
	mistakes = ""

	for i in range(0, len(pages)):
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
	in_file = sys.argv[1]

	tree = et.parse(in_file)
	root = tree.getroot()
	pages = root.findall('page')

	
	for e in pages:
		sentences = e.findall('sentence')
		temp = []
		

		for s in sentences:
			temp.append(s.text)

		
		dots = check_dots(temp)
		if len(dots) > 0:
			print "kesalahan titik pada halaman "+ e.attrib['id'] +"\n"+dots

		comma = check_comma(temp)
		if len(comma) > 0:
			print "kesalahan koma pada halaman "+ e.attrib['id'] +" "+comma

		semicolon = check_semicolon(temp)
		if len(semicolon) > 0:
			print "kesalahan titik koma pada halaman "+ e.attrib['id'] +" "+semicolon

		colon = check_colon(temp)
		if len(colon) > 0:
			print "kesalahan titik dua pada halaman "+ e.attrib['id'] +" "+colon
	

if __name__ == '__main__':
	main()