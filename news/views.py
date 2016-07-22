# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect
from news.parser import go_news_commit, go_news_wed
from django.utils import timezone
from datetime import datetime
from news.models import News
from logs.models import Logs
from local_site.settings import LOGSTATUSYES, LOGSTATUSNO
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response
from django.template import RequestContext

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
            
            log = Logs(
                    log_user = request.user, 
                    log_type = 7, 
                    log_status = LOGSTATUSYES,
                    )
            log.save()
            state = {
                'state_type':'success',
                'state_message':'<strong>Отлично!</strong> Все прошло как надо! Добавлено коммитов: %s' % (len(all_commits)),
                    }
            data = {
                'news_commit': all_commits,
                'state':state,
                }
            return render(request,
                            'admin/readd_all_commits.html',
                            data,)
        except Exception as inst:
            import sys
            log = Logs(
                    log_user = request.user, 
                    log_type = 7, 
                    log_status = LOGSTATUSNO,
                    )
            log.save()
            state = {
                'state_type':'danger',
                'state_message':inst,
                    }
            data  = {
                'state':state,
                    }
            return render(request,
                            'admin/readd_all_news_wed.html',
                            data,)

    else:
        return HttpResponseRedirect('/')

def readd_all_news_wed(request):
    if request.user.is_superuser:
        try:
            all_commits = go_news_wed()
            News.objects.filter(news_type=1).delete()
            for news_date, news_text in all_commits.items():
                news_item = News(
                            title = news_text,
                            created_date = datetime.strptime(news_date, '%Y-%m-%d %H:%M:%S'),
                            news_type = 1,
                            parsed_date = timezone.now(),
                            )
                news_item.save()
            log = Logs(
                    log_user = request.user, 
                    log_type = 6, 
                    log_status = LOGSTATUSYES,
                    )
            log.save()
            state = {
                'state_type':'success',
                'state_message':'<strong>Отлично!</strong> Все прошло как надо! Добавлено новостей: %s' % (len(all_commits)),
                    }
            data = {
                'news_commit': all_commits,
                'state':state,
                }
            return render(request,
                            'admin/readd_all_news_wed.html',
                            data,)
        except Exception as inst:
            import sys
            log = Logs(
                    log_user = request.user, 
                    log_type = 6, 
                    log_status = LOGSTATUSNO,
                    )
            log.save()
            state = {
                'state_type':'danger',
                'state_message':inst,
                    }
            data  = {
                'state':state,
                    }
            return render(request,
                            'admin/readd_all_news_wed.html',
                            data,)
    else:
        return HttpResponseRedirect('/')


def all_news(request, news_type='all'):
    if news_type=='all':
        all_news = News.objects.all().order_by('-created_date')
        news_type = 'Все новости'
    elif news_type=='commits':
        all_news = News.objects.filter(news_type=2).order_by('-created_date')
        news_type = 'Новости разработчика'
    elif news_type=='wimagic':
        all_news = News.objects.filter(news_type=1).order_by('-created_date')
        news_type = 'Новости провайдера'
    else:
        return HttpResponseRedirect('/')

    paginator = Paginator(all_news, 8)
    page = request.GET.get('page')
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)
    vars = dict(
        news=news,
        news_type=news_type,
        )
    return render_to_response(
                    'news/news.html', 
                    vars, 
                    context_instance=RequestContext(request)
                    )
        # 'commits':News.objects.filter(news_type=2).order_by('-created_date')[:3],
        # 'news_wed':News.objects.filter(news_type=1).order_by('-created_date')[:3],