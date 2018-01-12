#!/usr/bin/env python -W ignore::DeprecationWarning
# -*- coding: utf-8 -*-qq

import sys
from bs4 import BeautifulSoup

in_file = sys.argv[1]
errors = {	
			"TYPO":0,
			"PUNCT":0,
			"SPACE":0,
			"PARALELLISM":0,
			"INCOMPLETE":0,
			"EFF":0,
			"CAPITAL":0,
			"ITALIC":0,
			"ABBR":0,
			"REDUNDANT":0,
			"CONJ":0,
			"TRANS":0,
			"STANDARD":0,
			"VERB":0,
			"PRONOUN":0,
			"PREP":0,
			"LOGIC":0,
			"CHANGE":0,
			"":0
		}

with open(in_file, 'r') as f:
	soup = BeautifulSoup(f, 'xml')

pair = soup.find_all("PAIR")

for p in pair:
	key = "".join(str(e) for e in p.ERRTYPE.contents)

	errors[key] += 1

print "\n"
for key, value in errors.iteritems():
	if key == "":
		print "Unannotated: " + str(value)
	else:
		print key + ": " + str(value)

print "Total Pair: " + str(len(pair))