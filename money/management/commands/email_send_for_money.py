from django.core.management.base import BaseCommand
from money.models import Post, Tarif
from django.contrib.auth.models import User

from logs.models import Logs
from userprofile.models import UserProfile

import requests
import lxml.html

from local_site.settings import TYPE_CHOICES, LOGSTATUSYES, LOGSTATUSNO

# python manage.py moneyparse

def sender_email():
    """
    Нужно чтоб были импортированы:
    UserProfile, User, Post, Logs
    requests, lxml.html
    """
    for i in User.objects.filter(is_superuser=False):
        money_last = Post.objects.filter(user=i).last()
        print (money_last.money)
    return 'yo'


class Command(BaseCommand):
    # Задаём текст помощи, который будет
    # отображён при выполнении команды
    # python manage.py createtags --help
    help = 'Auto money check for all users'

    def handle(self, *args, **options):
        self.stdout.write(sender_email())
