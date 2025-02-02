#!/usr/bin/env python -W ignore::DeprecationWarning
# -*- coding: utf-8 -*-qq

import sys
import re
import optparse
import xml.etree.ElementTree as et

def config():
	reload(sys)
	sys.setdefaultencoding('utf-8')


def extract_xml(argv):
	in_file = sys.argv[1]

	tree = et.parse(in_file)
	pages = tree.getroot()
	allpage = pages.findall("page")

	# heading dokumen XML
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
					
					# penutup tag bold dan italic jika flag = 1
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
						# berikan tag italic jika flag = 0 dan ditemukan atribut italic
						if "Italic" in t.attrib['font'] and flag_it == 0:
							flag_it = 1

							if line is "" or not line[-1].isalpha():
								line = line + "<it>"
						
						# berikan tag bold jika flag = 0 dan ditemukan atribut Bold
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

				# mendadai segmen dan title dari dokumen
				if re.match('[0-9]+\.+[0-9]+\.+[0-9]*\.*\s+', trim) is not None or (trim.isupper() and "." not in trim) :
					if flag_seg == 0:
						segment = segment + "\n\t\t</segment>" + "\n\t\t<title>" + item[:-1] + "</title>"
						flag_seg = 1
					else:
						segment = segment + "\n\t\t<title>" + item[:-1] + "</title>"
						flag_seg = 1

				# tandai Universitas Indonesia sebagai footer
				elif "<bo>Universitas</bo> <bo>Indonesia</bo>" in item:
					
					if flag_seg == 0:
						segment = segment + "\n\t\t</segment>" + "\n\t\t<footer>" + item[:-1] + "</footer>"
						flag_seg = 1
					else:
						segment = segment + "\n\t\t<footer>" + item[:-1] + "</footer>"
						flag_seg = 1
				
				# regex untuk mencari nomor halaman dan menandai dengan tag pagenum
				elif (trim.strip().isdigit() and len(trim.strip()) <= 4) or (re.match(r'\b[vix]+\b(?![,])', trim) is not None and len(trim.strip()) <= 4):
					if flag_seg == 0:
						segment = segment + "\n\t\t</segment>" + "\n\t\t<pagenum>" + item[:-1] + "</pagenum>"
						flag_seg = 1
					else:
						segment = segment + "\n\t\t<pagenum>" + item[:-1] + "</pagenum>"
						flag_seg = 1
				else:
					if flag_seg == 1:
						segment = segment + "\n\t\t<segment>\n\t\t\t" + item
						flag_seg = 0
					else:
						segment = segment + item
		
		#  tag yang menandai suatu halaman
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

	parser = optparse.OptionParser()
	parser.add_option('-o', action="store")

	options, args = parser.parse_args()

	with open(options.o, 'w') as f:
		f.write(a)



if __name__ == '__main__':
	main()