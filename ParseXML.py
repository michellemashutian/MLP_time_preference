#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: mashutian
@time: 2019-02-28 21:14
@desc: parse xml to get time
"""

# -*- coding: utf-8 -*-
import os
import re
import xml.etree.ElementTree as ET


def sj(a, b):
    return (a + '\t' + b).strip()


def j(a, b):
    if a == b:
        return True


# 去标签
def wipe(name):
    string = re.sub(r'</?[^>]+>', ' ', name)
    string = re.sub(r'\s+', ' ', string)
    return string.strip()


# 过滤四字节字符
def filter_str(s):
    highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    string = highpoints.sub(u'??', s)
    return string


# 计数器
count = 1

# ploscontent
result = open(r'/Volumes/SaveMe/data/2019/pubmed/id-year-add', 'w')
Findpath = r'/Volumes/SaveMe/data/2019/pubmed/noyear-xml'
filenames = os.listdir(Findpath)
for name in filenames:
    count = count + 1
    filepath = os.path.join(Findpath, name)
    fileop = open(filepath)
    text = fileop.read()
    tree = ET.parse(filepath)



    # pubtime = re.findall(r"<MedlineDate>(.+?)</MedlineDate>", text)
    # if len(pubtime)!= 1:
    #     print pubtime
    #     print "第" + str(count) + "个文件：" + name
    #     pubdate = re.findall(r"<PubDate>(.+?)</PubDate>", text)
    #     print pubdate

result.close()




