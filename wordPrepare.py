#!/usr/bin/env python
import sys
import importlib
importlib.reload(sys)
import re
import jieba
jieba.load_userdict('./textfile/split_list.txt')
import csv

datafile = open('./textfile/grepOther1101', 'r')
stop_list = {}.fromkeys([line.strip() for line in open('./textfile/stop_words.txt')])
name_list = {}.fromkeys([line.strip() for line in open('./textfile/name.txt')])

result = list()
line = datafile.readline()
while line:
	line_array = line.split('\t')
	content = re.sub(r'http://t.cn/\w{7}', '', line_array[2])
	content = content.replace('\xe2\x80\x8b', '')
	content = re.sub(u'\\#.*?#|\\[.*?]|\\\\n', '', content)
	content_only = re.sub(u'[^a-zA-Z\u4e00-\u9fa5]', ' ', content)

	word_seg = jieba.cut(content_only.strip())

	word_seg = [ word for word in list(word_seg) ]
	word_seg = [ word for word in list(word_seg) if word not in stop_list ]     # 790K
	word_seg = [ word for word in list(word_seg) if word not in name_list ]     # 769K
	word = [ x for x in word_seg if x not in ['', ' ', '\t', '\n'] ]            # 636K
	word = [ x for x in word if len(x) > 1 ]
	less_dup = []
	c = []
	counter = 0
	for i in word:
		c = word[counter:]
		if i in c[1:]:
			less_dup.append(c[0])
		else:
			if i not in less_dup:
				less_dup.append(c[0])
			else:
				pass
		counter += 1
	if len(less_dup) != 0:
		newlist = ' '.join(less_dup)
		if len(newlist.split()) > 1:
			print(newlist)
		else:
			pass
	else:
		pass
	line = datafile.readline()
datafile.close()
