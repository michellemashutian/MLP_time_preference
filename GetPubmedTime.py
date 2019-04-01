#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: mashutian
@time: 2019-02-28 20:46
@desc: get time information based on pubmed id
"""

# import re
# import urllib2
import requests
# import lxml
# from bs4 import BeautifulSoup
import time
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id=11442208'
# ids = url[83:]
# #page=urllib2.urlopen(url)
# page = requests.get(url).text
# result = open('/Volumes/SaveMe/data/2019/pubmed/noyear-xml/'+ids, 'w')
# result.write(page)
# result.close()

count = 0
with open('/Volumes/SaveMe/data/2019/pubmed/no-year-url-5', 'r') as f:
    for line in f:
        url = line.strip()
        api = url.index("api")-1
        ids = url[83:api]
        # #page=urllib2.urlopen(url)
        page = requests.get(url).text
        result = open('/Volumes/SaveMe/data/2019/pubmed/noyear-xml/'+ids, 'w')
        result.write(page)
        result.close()
        time.sleep(2)
        count = count + 1
        print count

        # pagesoup = BeautifulSoup(page, 'lxml')
        # for link in pagesoup.find_all(name='a',attrs={"href":re.compile(r'^http:')}):
        #     print link.get_text()