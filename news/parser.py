# -*- coding:utf-8 -*-

from lxml import etree, html
import lxml.html
import requests
from lxml.cssselect import CSSSelector

r = requests.get('http://www.wimagic.com.ua/ua/news')
doc = lxml.html.fromstring(r.text)



    #main > div.blog > div.items-row.cols-1.row-0.row-fluid.clearfix > div > div
    #main > div.blog > div.items-row.cols-1.row-0.row-fluid.clearfix > div > div > div > h2
    #main > div.blog > div.items-row.cols-1.row-0.row-fluid.clearfix > div > div > dl > dd
    #main > div.blog > div.items-row.cols-1.row-0.row-fluid.clearfix > div > div > dl > dd > time
    #main > div.blog > div.items-row.cols-1.row-0.row-fluid.clearfix > div > div > d
    #main > div.items-row.cols-1.row-0.row-fluid.clearfix div div dl dd time

for div in doc.cssselect('div.clearfix'):
	print(div.cssselect(' div div div h2')[0].text_content().replace('	', '').replace('\n',''))
	print(div.cssselect(' div div dl dd time')[0].text_content().replace('	', '').replace('\n',''))
	# print(div.cssselect('time')[0].text_content())
	# print(div.text_content().replace('	', '').replace('\n',''))

