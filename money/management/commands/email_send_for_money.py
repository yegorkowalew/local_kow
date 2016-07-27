from django.core.management.base import BaseCommand
from money.models import Post, Tarif
from django.contrib.auth.models import User
from logs.models import Logs
from userprofile.models import UserProfile
# from local_site.settings import TYPE_CHOICES, LOGSTATUSYES, LOGSTATUSNO

# python manage.py email_send_for_money
from datetime import datetime, timedelta
from django.utils import timezone
from number_to_text import num2text

from django.template.loader import get_template
from django.template.loader import render_to_string
from django.core.mail import send_mail
from local_site.settings import EMAIL_HOST_USER

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
    Выбрал пользователей, добавляю каждому пользователю метку о состоянии счета.


    """
    tdelta = timedelta(seconds=50)
    male_units = ((u'день', u'дня', u'дней'), 'm')
    users = User.objects.filter(is_superuser=False)
    for user in users:
        money_last = Post.objects.filter(user=user).order_by('created_date').last()
        if money_last.money < 50 and true_log(user, tdelta):
            subject = 'У Вас уже меньше 50грн. на балансе.'
            tarif_last = Tarif.objects.filter(user=user).last()
            user.money_state = 'zero'
            user.subject = subject
            user.context = {
                'title': subject, 
                'pr_user': UserProfile.objects.get(user_id=user.id),
                'money_last': money_last.money,
                'tarif_last':tarif_last.money_for_mons/30,
                'days_left': num2text(round(money_last.money/(tarif_last.money_for_mons/30)), male_units),
                }
            # user.txt = render_to_string('email/on_50.txt', context)
            # user.html = render_to_string('email/on_50.html', context)


    return 'yo'

class Command(BaseCommand):
    # Задаём текст помощи, который будет
    # отображён при выполнении команды
    # python manage.py createtags --help
    help = 'Auto money check for all users'

    def handle(self, *args, **options):
        sender_email()
        # switch_case()
        # raw_input("Input a number between 1 and 3: ")
        # print(timedelta(seconds=50))
        # test_users(User.objects.filter(is_superuser=False))

def e_send_on_50(request):
    subject = 'У Вас уже меньше 50грн. на балансе.'
    money_last = Post.objects.filter(user=request.user).order_by('created_date').last()
    tarif_last = Tarif.objects.filter(user=request.user).last()
    male_units = ((u'день', u'дня', u'дней'), 'm')
    # (tarif_last.money_for_mons/30)
    context = {
        'title': subject, 
        'pr_user': UserProfile.objects.get(user_id=request.user.id),
        'money_last': money_last,
        'tarif_last':tarif_last.money_for_mons/30,
        'days_left': num2text(round(money_last.money/(tarif_last.money_for_mons/30)), male_units),
        'request':request,
        }

    txt = render_to_string('email/on_50.txt', context)
    html = render_to_string('email/on_50.html', context)

    send_mail(subject, txt, EMAIL_HOST_USER, ['kowalew.backup@gmail.com'], 
          fail_silently=False, html_message=html)