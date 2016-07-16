# -*- coding:utf-8 -*-

import requests
import lxml.html

import lxml
from lxml.html.clean import clean_html

filename = '/home/yegor/local_kow/news/file.html'

root = lxml.html.parse(filename).getroot()
parser = lxml.html.HTMLParser(encoding='utf-8')
root = lxml.html.parse(filename, parser=parser).getroot()
els = root.cssselect('div.page-header h2')

# el_text = els[0].text
# el_href = els[0].attrib['href']

# print(els[0].tostring(html))

# print(lxml.html.tostring(els[0]))
# print (lxml.html.tostring(els[0]))

# print(lxml.html.tostring(els[0]))

# lxml.html.tostring(els[0])

from lxml.etree import tostring

html = clean_html(els[0])

result = lxml.html.tostring(html, encoding="utf-8").decode("utf-8")
# print(result.strip())


# print(tostring(result, pretty_print=True).strip())

# html body div.contentbg div.cntbottom div#contenttxt div.content div#main div.blog div.items-row.cols-1.row-0.row-fluid.clearfix

# div.page-header h2