# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect
from news.parser import go_news_commit
from django.utils import timezone
from datetime import datetime
from news.models import News
from logs.models import Logs
from local_site.settings import LOGSTATUSYES, LOGSTATUSNO

def readd_all_commits(request):
    if request.user.is_superuser:
        try:
            all_commits = go_news_commit()
            # print(all_commits)
            News.objects.filter(news_type=2).delete()
            for news_date, news_text in go_news_commit().items():
                # print(news_date, news_text)
                created_date = datetime.strptime(news_date, '%Y-%m-%d %H:%M:%S')
                print(created_date)
                news_item = News(
                            title = news_text,
                            created_date = datetime.strptime(news_date, '%Y-%m-%d %H:%M:%S'),
                            news_type = 2,
                            parsed_date = timezone.now(),
                            )
                news_item.save()

            data = {
                'news_commit': go_news_commit(),
            }
            
            log = Logs(log_user = request.user, log_type = 7, log_status = LOGSTATUSYES,)
            log.save()

            return render(request,
                            'admin/readd_all_commits.html',
                            data,)
        except:
            print('no')
            log = Logs(log_user = request.user, log_type = 7, log_status = LOGSTATUSNO,)
            log.save()
            return HttpResponseRedirect('/')

    else:
        return HttpResponseRedirect('/')

# def readd_all_commits(request):
#     all_commits = go_news_commit()
#     # print(all_commits)
#     News.objects.filter(news_type=2).delete()
#     for news_date, news_text in go_news_commit().items():
#         # print(news_date, news_text)
#         created_date = datetime.strptime(news_date, '%Y-%m-%d %H:%M:%S')
#         print(created_date)
#         news_item = News(
#                     title = news_text,
#                     created_date = datetime.strptime(news_date, '%Y-%m-%d %H:%M:%S'),
#                     news_type = 2,
#                     parsed_date = timezone.now(),
#                     )
#         news_item.save()

#         data = {
#             'news_commit': go_news_commit(),
#         }
            
#         log = Logs(log_user = request.user, log_type = 7, log_status = LOGSTATUSYES,)
#         log.save()

#         return render(request,
#                         'admin/readd_all_commits.html',
#                         data,)