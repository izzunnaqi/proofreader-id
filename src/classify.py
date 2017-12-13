#!/usr/bin/env python -W ignore::DeprecationWarning
# -*- coding: utf-8 -*-qq

import sys
import re
import feature
from sklearn import svm
from sklearn import metrics
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from bs4 import BeautifulSoup


def config():
	reload(sys)
	sys.setdefaultencoding('utf-8')

def get_pair(xmldoc):
	res = []

	with open(xmldoc) as fp:
		soup = BeautifulSoup(fp, 'xml')

	pair = soup.find_all('PAIR')

	for p in pair:
		before = "".join(str(e) for e in p.BEFORE.contents)
		after = "".join(str(e) for e in p.AFTER.contents)
		res.append([before, after])

	return res

def extract_class(xmldoc):
	err = []

	with open(xmldoc) as fp:
		soup = BeautifulSoup(fp, 'xml')

	pair = soup.find_all('PAIR')

	for p in pair:
		c = "".join(str(e) for e in p.ERRTYPE.contents)
		err.append(c)

	return err

def feature_generata(pair):
	ftr = feature.Feature()
	res = []

	for x, y in pair:
		fc = ftr.first_capital(x, y)
		cd = ftr.capital_diff(x, y)
		sld = ftr.sent_lenght_diff(x, y)
		cod = ftr.comma_diff(x, y)
		dd = ftr.dot_diff(x, y)
		it = ftr.italic_diff(x, y)
		cb = ftr.count_bigram(x, y)
		cp = ftr.count_postag(x, y)

		res.append([fc, cd, sld, cod, dd, it, cb, cp])

	return res

def main():
	config()
	train_in = sys.argv[1]
	# test_in = sys.argv[2]

	train_pair = get_pair(train_in)
	pair_label = extract_class(train_in)
	# test_pair = get_pair(test_in)

	pair_data = feature_generata(train_pair)
	model = svm.SVC(kernel='linear', C=1)

	# predicted = cross_val_predict(model, pair_data, pair_label, cv=7)
	# correct = 0
	# for i in xrange(len(predicted)):
	# 	print pair_label[i] , predicted[i]
	# 	if pair_label[i] == predicted[i]:
	# 		correct += 1

	# print "\nCorrect: " + str(correct)


	for i in xrange(2, 10):
	
		scores = cross_val_score(model, pair_data, pair_label, cv=i)
		print "Scores " + str(i) + "-folds"
		print scores

		predicted = cross_val_predict(model, pair_data, pair_label, cv=i)
		acc = metrics.accuracy_score(pair_label, predicted) 
		print "Accuracy: " + str(acc)

		print "====================\n"

	# print "<CORPUS>"
	# m = len(res)
	# i = 0
	# while i < m:
	# 	print "<PAIR>"
	# 	print "<BEFORE>" + test_pair[i][0] + "</BEFORE>"
	# 	print "<AFTER>" + test_pair[i][1] + "</AFTER>"
	# 	print "<ERRTYPE>" + res[i] + "</ERRTYPE>"
	# 	print "</PAIR>"
	# 	print
	# 	i += 1
	# print "</CORPUS>"

if __name__ == '__main__':
	main()

