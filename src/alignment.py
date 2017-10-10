#!/usr/bin/env python -W ignore::DeprecationWarning
# -*- coding: utf-8 -*-qq

import sys
import re
import xml.etree.ElementTree as et

def config():
	reload(sys)
	sys.setdefaultencoding('utf-8')


def align(arg1, arg2):
	in1 = et.parse(arg1)
	doc1 = in1.getroot()
	allpage_1 = doc1.findall("page")

	in2 = et.parse(arg2)
	doc2 = in2.getroot()
	allpage_2 = doc2.findall("page")

	match = []

	for 

def main():
	config()
	
	

if __name__ == '__main__':
	main()
