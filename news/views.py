# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect
from news.parser import go_news_commit
from django.utils import timezone
from datetime import datetime
from news.models import News

def readd_all_commits(request):
    if request.user.is_superuser:
        try:
            all_commits = go_news_commit()
            News.objects.filter(news_type=2).delete()
            for news_date, news_text in go_news_commit().items():
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
            return render(request,
                            'admin/readd_all_commits.html',
                            data,)
        except:
            return HttpResponseRedirect('/')

    else:
        return HttpResponseRedirect('/')
    