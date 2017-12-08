#!/usr/bin/env python -W ignore::DeprecationWarning
# -*- coding: utf-8 -*-qq

import sys
import re
import nltk
from bs4 import BeautifulSoup
from polyglot.text import Text


class Feature():

	def first_capital(self, x, y):
		x = re.sub("<it>|</it>|<bo>|</bo>", "", x)
		y = re.sub("<it>|</it>|<bo>|</bo>", "", y)

		if x[0].isupper() and y[0].isupper():
			return 0
		else:
			return 1

	def capital_diff(self, x, y):
		cx = 0
		for e in x: 
			if e.isupper(): cx+=1
		
		cy = 0
		for e in y: 
			if e.isupper(): cy+=1

		return abs(cx - cy)

	def sent_lenght_diff(self, x, y):
		x = x.replace("  ", " ")
		y = y.replace("  ", " ")

		wordx = x.split(" ")
		wordy = y.split(" ")

		return abs(len(wordx) - len(wordy))

	def comma_diff(self, x, y):
		cx = 0
		for e in x: 
			if e == "," : cx+=1
		
		cy = 0
		for e in y: 
			if e == "," : cy+=1

		return abs(cx - cy)

	def dot_diff(self, x, y):
		cx = 0
		for e in x: 
			if e == "." : cx+=1
		
		cy = 0
		for e in y: 
			if e == "." : cy+=1

		return abs(cx - cy)

	def italic_diff(self, x, y):
		x = x.replace("  ", " ")
		y = y.replace("  ", " ")

		wordx = x.split(" ")
		wordy = y.split(" ")

		cx = 0
		for w in wordx:
			if "<it>" in w: cx+=1

		cy = 0
		for w in wordy:
			if "<it>" in w: cy+=1

		return abs(cx - cy)

	def count_bigram(self, x, y):
		x = x.replace("  ", " ")
		y = y.replace("  ", " ")

		wordx = x.split(" ")
		wordy = y.split(" ")

		bx = list(nltk.bigrams(wordx))
		by = list(nltk.bigrams(wordy))

		count = 0
		for a, b in bx:
			strx = " ".join((a, b))

			for c, d in by:
				stry = " ".join((c, d))

				if strx == stry:
					count += 1

		return count

	def count_postag(self, x, y):
		x = x.replace("  ", " ")
		y = y.replace("  ", " ")

		tx = Text(x, hint_language_code='id')
		ty = Text(y, hint_language_code='id')

		px = tx.pos_tags
		py = ty.pos_tags

		count = 0
		i = 0
		while (i < len(px) and i < len(py)):
			if px[i][1] == py[i][1]:
				count += 1
			i += 1

		return count
