#!/usr/bin/env python -W ignore::DeprecationWarning
# -*- coding: utf-8 -*-qq

import sys
import re
import feature
import itertools
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.svm import SVC, LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_fscore_support, accuracy_score
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import StratifiedShuffleSplit
from bs4 import BeautifulSoup

errors = [
			"TYPO",
			"PUNCT",
			"SPACE",
			"PARALELLISM",
			"INCOMPLETE",
			"EFF",
			"CAPITAL",
			"ITALIC",
			"ABBR",
			"REDUNDANT",
			"CONJ",
			"TRANS",
			"STANDARD",
			"VERB",
			"PRONOUN",
			"PREP",
			"LOGIC",
			"CHANGE"
		]


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

def classify_error(clf, pair_data, pair_label):	
	skf = StratifiedKFold(n_splits=10)

	predicted = cross_val_predict(clf, pair_data, pair_label, cv=skf)
	scores = cross_val_score(clf, pair_data, pair_label, cv=skf)

	return predicted


def evaluate(pair_label, predicted, name):
	acc = accuracy_score(pair_label, predicted)
	precision, recall, fscore, support = precision_recall_fscore_support(pair_label, predicted, average='micro')

	print '%s :'% name
	print '\taccuracy: {}'.format(acc)
	print '\tprecision: {}'.format(precision)
	print '\trecall: {}'.format(recall)
	print '\tf1: {}\n'.format(fscore)

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
	
    plt.rc('font', size=11)  
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.tick_params(axis='y', labelsize=10, right=False, top=False, direction="out")
    plt.tick_params(axis='x', labelsize=9, right=False, bottom=False, direction="out", labelbottom=False, labeltop=True)
    plt.xticks(tick_marks, classes, rotation=70)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center", va="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')		
    ax = plt.gca()
    ax.xaxis.set_label_position("top")
    plt.tight_layout()

def feature_generate(pair):
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
		sim = ftr.similarity(x, y)

		res.append([fc, cd, sld, cod, dd, it])

	return res  

def main():
	config()
	train_in = sys.argv[1]

	train_pair = get_pair(train_in)
	pair_label = extract_class(train_in)

	pair_data = feature_generate(train_pair)

	print '=================================================='
	print 'Feature Set: fc, cd, sld, cod, dd, it'
	print '=================================================='
	pred_svm = classify_error(SVC(), pair_data, pair_label)

	
	evaluate(pair_label, pred_svm, "SVC")
	# cm = confusion_matrix(pair_label, pred_svm, labels=errors)
	# plot_confusion_matrix(cm, classes=errors)
	# plt.savefig("conf-mat-svm.png")
	
	pred_lsvm = classify_error(LinearSVC(), pair_data, pair_label)
	evaluate(pair_label, pred_lsvm, "Linear SVC")
	
	pred_nb = classify_error(GaussianNB(), pair_data, pair_label)
	evaluate(pair_label, pred_nb, "Naive Bayes")
	
	pred_lr = classify_error(LogisticRegression(), pair_data, pair_label)
	evaluate(pair_label, pred_lr, "Logistic Regression")
	
	pred_rf = classify_error(RandomForestClassifier(), pair_data, pair_label)
	evaluate(pair_label, pred_rf, "Random Forest")



if __name__ == '__main__':
	main()

