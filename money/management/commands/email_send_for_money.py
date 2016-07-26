from django.core.management.base import BaseCommand
from money.models import Post, Tarif
from django.contrib.auth.models import User
from logs.models import Logs
from userprofile.models import UserProfile
# from local_site.settings import TYPE_CHOICES, LOGSTATUSYES, LOGSTATUSNO

# python manage.py email_send_for_money
from datetime import datetime, timedelta
from django.utils import timezone

def sender_email():
    """
    Нужно чтоб были импортированы:
    UserProfile, User, Post, Logs
    requests, lxml.html
    """
    tdelta = timedelta(seconds=50)

    for user in User.objects.filter(is_superuser=False):
        money_last = Post.objects.filter(user=user).last()
        print(money_last.money)
        ld = Logs.objects.filter(log_user=user, log_type=2).last()
        if ld == None:
            ld = 0
        # if ld != None:
        #     if ld.log_date + tdelta > timezone.now():
        #         print('Еще не прошло время')
        #     else:
        #         print('Время вышло')

        if money_last.money < 50 and (ld.log_date + tdelta > timezone.now()):
            print('надо засылать')
        
        if True and False or True:
            print('test')

    return 'yo'

class Command(BaseCommand):
    # Задаём текст помощи, который будет
    # отображён при выполнении команды
    # python manage.py createtags --help
    help = 'Auto money check for all users'

    def handle(self, *args, **options):
        sender_email()
        # print(timedelta(seconds=50))
