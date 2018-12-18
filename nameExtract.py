#!/usr/bin/env python
import sys
import importlib
importlib.reload(sys)
import re

with open('./textfile/id_name.txt') as f:
    content = f.readlines()
content = [x.strip() for x in content]
# r = re.compile('.*musicPerson.*|.*moviePerson.*')
r = re.compile('.*1042015:movie_.*')
newList = list(filter(r.match, content))
for i in newList:
    print(i.split('\t',1)[1])
