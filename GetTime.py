#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: mashutian
@time: 2019-02-28 18:47
@desc: get year information for all
"""
year = {}

result1 = open('/Volumes/SaveMe/data/2019/pubmed/no-year-id', 'w')

with open('/Volumes/SaveMe/data/2019/pubmed/id-year.txt', 'r') as f:
    for line in f:
        xx = line.strip().split('\t')
        year[xx[0]] = xx[1]

yearcount = {}
count = 0
with open('/Volumes/SaveMe/data/2019/pubmed/truth/test-re', 'r') as f:
    for line in f:
        if line.strip() in year:
            continue
            # pubyear = year[line.strip()]
            # if pubyear in yearcount:
            #     oldcount = yearcount[pubyear]
            #     yearcount[pubyear] = oldcount + 1
            # else:
            #     yearcount[pubyear] = 1
        else:
            count = count + 1
            result1.write(line.strip()+'\n')

print count
result1.close()
# for i in yearcount:
#     print i, yearcount[i]


