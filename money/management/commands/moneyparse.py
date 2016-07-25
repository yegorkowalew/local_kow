from django.core.management.base import BaseCommand
from money.models import Post, Tarif
from django.contrib.auth.models import User

from logs.models import Logs
from userprofile.models import UserProfile

import requests
import lxml.html

from local_site.settings import TYPE_CHOICES, LOGSTATUSYES, LOGSTATUSNO

# python manage.py moneyparse

def money_check(check_user):
    """
    Нужно чтоб были импортированы:
    UserProfile, User, Post, Logs
    requests, lxml.html
    """
    pr_user = UserProfile.objects.get(user_id=check_user.id)    
    try:
        r = requests.post(
                 'http://www.wimagic.com.ua/1.php', 
                 # 'http://www.wimagicss.com.ua/1.php', 
                data = {
                    'login':check_user.username, 
                    'pass':pr_user.pwd
                        }
                    )
        html = lxml.html.fromstring(r.text)
        money_r = html.xpath("/html/body/table/tr[1]/td[4]/text()")[0]

        new = Post(money=money_r, user=check_user)
        new.save()
        
        log = Logs(log_user = check_user, log_type = 1, log_status = LOGSTATUSYES,)
        log.save()
        # return 1
    except:
        log = Logs(log_user = check_user, log_type = 1, log_status = LOGSTATUSNO,)
        log.save()
        # return 0

class Command(BaseCommand):
    # Задаём текст помощи, который будет
    # отображён при выполнении команды
    # python manage.py createtags --help
    help = 'Auto money check for all users'

    def handle(self, *args, **options):
        money_pay_users = User.objects.filter(is_superuser=False)

        for i in money_pay_users:
            money_check(i)
            # self.stdout.write(i.username)

#