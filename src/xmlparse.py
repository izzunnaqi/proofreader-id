#!/usr/bin/env python
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
	page = pages.find("page")
	allpage = pages.findall("page")

	temp = ''
	pages = {}
	textbox = page.findall("textbox")

	temp = "<?xml version=\"1.0\" encoding=\"utf-8\" ?>\n<document>\n"
	for p in allpage:
		temp = temp + '<page id=\"'+ p.attrib['id']+'\">'

		for el in p.findall("textbox"):
			for t in el.findall("textline/text"):
				if 'bbox' in t.attrib:
					if t.text is None:
						temp = temp + " "
					else:
						if t.text == '&':
							temp = temp + '&amp;'
						elif t.text == '>':
							temp = temp + "&gt;"
						elif t.text == '<':
							temp = temp + "&lt;"
						else:
							temp = temp + t.text

					# temp = temp.rstrip("\n" )

			temp = temp + '\n'

		temp = temp + '</page>\n'

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