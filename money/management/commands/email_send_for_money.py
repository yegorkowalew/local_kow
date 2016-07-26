from django.core.management.base import BaseCommand
from money.models import Post, Tarif
from django.contrib.auth.models import User
from logs.models import Logs
from userprofile.models import UserProfile
# from local_site.settings import TYPE_CHOICES, LOGSTATUSYES, LOGSTATUSNO

# python manage.py email_send_for_money
from datetime import datetime, timedelta
from django.utils import timezone

def true_log(user, tdelta):
    ld = Logs.objects.filter(log_user=user, log_type=2).last()
    if ld == None:
        return True
    if ld.log_date + tdelta > timezone.now():
        return False # отсылаем. 
    else:
        return True

def sender_email():
    """
    Нужно чтоб были импортированы:
    UserProfile, User, Post, Logs
    requests, lxml.html
    """
    zero=[]
    twenty=[]
    fifty=[]
    tdelta = timedelta(seconds=50)
    for user in User.objects.filter(is_superuser=False):
        money_last = Post.objects.filter(user=user).last()    
        if money_last.money < 0 and true_log(user, tdelta):
            print('zero ',user.username)
            zero.append(user)
        elif money_last.money < 20 and true_log(user, tdelta):
            print('twenty ',user.username)
            twenty.append(user)
        elif money_last.money < 50 and true_log(user, tdelta):
            print('fifty ',user.username)
            fifty.append(user)
    messages=[]
    messages=messages+zero+twenty+fifty
    print(messages)
    return 'yo'

def switch_case(case):
    return "You entered " + {
        '1' : "one",
        '2' : "two",
        '3' : "three"
    }.get(case, "an out of range number")

    num = raw_input("Input a number between 1 and 3: ")
    print(switch_case(num))

class Command(BaseCommand):
    # Задаём текст помощи, который будет
    # отображён при выполнении команды
    # python manage.py createtags --help
    help = 'Auto money check for all users'

    def handle(self, *args, **options):
        # sender_email()
        # switch_case()
        raw_input("Input a number between 1 and 3: ")
        # print(timedelta(seconds=50))
