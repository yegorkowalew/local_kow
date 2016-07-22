# -*- coding:utf-8 -*-

import lxml.html
import requests
from lxml.cssselect import CSSSelector
import git

def go_news_wed():
    """
    first = go_news_wed()
    for i, y in first.items():
        print(i)
        print(y)
    # print(list(news_list.keys())[0])
    """
    r = requests.get('http://www.wimagic.com.ua/ua/news')
    doc = lxml.html.fromstring(r.text)
    news_list = {}
    for div in doc.cssselect('div.clearfix'):
        # print(div.cssselect(' div div dl dd time[datetime]')[0].get('datetime').replace('T',' ').split('+')[0])
        # print(div.cssselect(' div div div h2')[0].text_content().replace('    ', '').replace('\n',''))
        news_list[div.cssselect(' div div dl dd time[datetime]')[0].get('datetime').replace('T',' ').split('+')[0]] = div.cssselect(' div div div h2')[0].text_content().replace('    ', '').replace('\n','')
    
    return news_list

def go_news_commit():
    """
    git log --pretty=format:"%ad - %s"
    git diff --shortstat краткая статистика по изменениям из последнего коммита
    print(list(list1.keys())[0])

    """
    g = git.Git("/home/yegor/local_kow/")
                # "/home/yegor/local_kow"
    # Работает дома:
    # commit_log = g.log("--date=format:%d-%m-%Y %H:%M:%S", "--pretty=format:" + '::%ad::%s').split('\n')

    # Работает на работе
    commit_log = g.log("--pretty=format:" + '::%ai::%s').split('\n')

    # git log --pretty=format:%ai -1
    # commit_log = g.log("--pretty=format:" + '::%ad::%s').split('\n')
    commit_list = {}
    for i in commit_log:
        i = i.split('::')
        # Работает дома
        # commit_list[i[1]] = i[2]

        # Работает на работе
        commit_list[i[1].split(' +')[0]] = i[2]
    return commit_list

# print (go_news_commit())
# print(list(go_news_commit())[0])
# print(list(go_news_commit().items())[0])
# print(list(go_news_wed().values())[0.)

# for dat, header in go_news_commit().items():
    # print(dat)
    # print(header)