# -*- coding:utf-8 -*-

# from lxml import etree, html
import lxml.html
import requests
from lxml.cssselect import CSSSelector

r = requests.get('http://www.wimagic.com.ua/ua/news')
doc = lxml.html.fromstring(r.text)

for div in doc.cssselect('div.clearfix'):
	print(div.cssselect(' div div div h2')[0].text_content().replace('	', '').replace('\n',''))
	print(div.cssselect(' div div dl dd time')[0].text_content().replace('	', '').replace('\n',''))

import git

g = git.Git("/home/yegor/local_site/local_kow/")
log = g.log("--pretty=format:" + '%ad - %s')
print(log)


# git log --pretty=format:"%ad - %s"

# git diff --shortstat краткая статистика по изменениям из последнего коммита