#!/usr/bin/env python
import sys
import importlib
importlib.reload(sys)
import numpy as np
np.set_printoptions(threshold=np.nan)
import random
from sklearn.svm import SVC
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


def input_file(filename):
	f = open(filename, 'r')
	line_list = f.readlines()
	return line_list


def label_positive(list_set):
	list_words = []
	for i in list_set:
		i = i.strip().split(' ')
		i.insert(0, '1')
		list_words.append(i)
	return list_words


def label_negative(list_set):
	list_words = []
	for i in list_set:
		i = i.strip().split(' ')
		i.insert(0, '-1')
		list_words.append(i)
	return list_words


def random_shuffle(train_words):
	random.Random(100).shuffle(train_words)
	return train_words


def split_set(list_words):
	x = []
	y = []
	for i in list_words:
		x.append(i[1:])
		y.append(i[0])
	return x, y


def tf_vectorize(train_x, test_x):
	v = TfidfVectorizer(tokenizer=None, binary=False, decode_error='ignore', stop_words='english')
	train_data = v.fit_transform(train_x)
	test_data = v.transform(test_x)
	vocab_dict = v.vocabulary_
	word = v.get_feature_names()
	return train_data, test_data, vocab_dict, word


def train_clf_svm(train_data, train_tags):
	clf = SVC(C=12000, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3,
	          gamma= 'auto', kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True,
	          tol=0.001, verbose=False)
	clf.fit(train_data, np.asarray(train_tags))
	# w = clf.coef_
	return clf


def train_clf_lr(train_data, train_tags):
	clf = LogisticRegression()
	clf.fit(train_data, np.asarray(train_tags))
	w = clf.coef_
	return clf, w


def interference(conflict_word, test_data, test_tags, pred):
	newlist = []
	for data, tag, elem_pred in zip(test_data, test_tags, pred):
		for x in data:
			if x in conflict_word and data not in newlist:
				newlist.append(data)
			else:
				pass
	return newlist


def evaluate(actual, pred):
	m_precision = metrics.precision_score(actual, pred, average='macro')
	m_recall = metrics.recall_score(actual, pred, average='macro')
	m_f1score = m_precision*m_recall*2/(m_precision+m_recall)
	print('precision:{0:.7f}'.format(m_precision))
	print('recall:{0:.7f}'.format(m_recall))
	print('f1 score:{0:.7f}'.format(m_f1score))

if __name__ == '__main__':
	filePositiveTrain = input_file('./textfile/segMovie')
	fileNegativeTrain = input_file('./textfile/segOther')
	fileTrain = input_file('./textfile/segCombine')

	filePositiveTest = input_file('./textfile/segMovieTest')
	fileNegativeTest = input_file('./textfile/segOtherTest')
	fileTest = input_file('./textfile/segCombineTest')

	wordPositiveTrain = label_positive(filePositiveTrain)
	wordNegativeTrain = label_negative(fileNegativeTrain)

	wordPositiveTest = label_positive(filePositiveTest)
	wordNegativeTest = label_negative(fileNegativeTest)

	wordTrain = wordPositiveTrain + wordNegativeTrain
	wordTest = wordPositiveTest + wordNegativeTest

	wordTrain = random_shuffle(wordTrain)
	wordTest = random_shuffle(wordTest)

	fileTrain = random_shuffle(fileTrain)
	fileTest = random_shuffle(fileTest)

	xTrain, yTrain = split_set(wordTrain)
	xTest, yTest = split_set(wordTest)

	tfidfTrain, tfidfTest, vocab_dict, word = tf_vectorize(fileTrain, fileTest)

	clf_svm, w_svm = train_clf_svm(tfidfTrain, yTrain)
	result_svm = clf_svm.predict(tfidfTest)
	evaluate(np.asarray(yTest), result_svm)

	clf_lr, w_lr = train_clf_lr(tfidfTrain, yTrain)
	result_lr = clf_lr.predict(tfidfTest)
	evaluate(np.asarray(yTest), result_lr)
