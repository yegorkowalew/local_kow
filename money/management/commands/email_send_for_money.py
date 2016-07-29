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

def numbers_to_template_name(argument):
    if argument < 0:
        return {'subject': 'Всё плохо', 'template_name': 'zero'}
    elif argument < 20:
        return {'subject': 'У Вас уже меньше 20грн. на балансе.', 'template_name': 'twenty'}
    elif argument < 50:
        return {'subject': 'У Вас уже меньше 50грн. на балансе.', 'template_name': 'fifty'}
    else:
        return False

from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

# ...

connection = mail.get_connection()
connection.open()
messages = list()

# for u in users:
#     c = Context({ 'first_name': u.first_name, 'reseller': self,})
#     subject, from_email, to = 'new reseller', settings.SERVER_EMAIL, u.email
#     text_content = plaintext.render(c)
#     html_content = htmly.render(c)
#     msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
#     msg.attach_alternative(html_content, "text/html")
#     messages.append(msg)

# connection.send_messages(messages)
# connection.close()


def sender_email():
    """
    Выбрал пользователей, добавляю каждому пользователю метку о состоянии счета.


    """
    tdelta = timedelta(seconds=50)
    male_units = ((u'день', u'дня', u'дней'), 'm')
    users = User.objects.filter(is_superuser=False)
    for user in users:
        money_last = Post.objects.filter(user=user).order_by('created_date').last()
        money_status = numbers_to_template_name(money_last.money)
        if money_status and true_log(user, tdelta):
            tarif = Tarif.objects.filter(user=user).last()
            print(tarif)
            if tarif:
                tarif_last = tarif.money_for_mons/30
                # print(tarif_last)
                days_left = num2text(round(money_last.money/(tarif.money_for_mons/30)), male_units)
                # print(days_left)
            # else:
                # tarif_last = '11'
                # print(tarif_last)
                # days_left = '11'
                # print(days_left)
            user.money_status = money_status
            user.title = money_status.get('subject')
            user.pr_user = UserProfile.objects.get(user_id=user.id)
            user.money_last = money_last.money
            user.tarif_last = tarif_last
            # print(user.tarif_last)
            user.days_left = days_left

    fifty_users = []
    zero_users = []
    twenty_users = []
    for user in users:
        if user.money_status.get('template_name') == 'fifty':
            context = Context({
                'title':user.title,
                'pr_user': user.pr_user,
                'money_last': user.money_last,
                'tarif_last': None,
                'days_left':'',# user.days_left,
                })

            # txt = render_to_string('email/on_50.txt', user.context)
            html = render_to_string('email/on_50.html', context)

    # send_mail(subject, txt, EMAIL_HOST_USER, ['kowalew.backup@gmail.com'], 
          # fail_silently=False, html_message=html)
            fifty_users.append(user)
        elif user.money_status.get('template_name') == 'twenty':
            twenty_users.append(user)
        elif user.money_status.get('template_name') == 'zero':
            zero_users.append(user)

    sorted_users = dict(fifty=fifty_users, zero=zero_users, twenty=twenty_users)

    # print(sorted_users)
    # for user in fifty_users:
        # print(user.money_status.get('template_name'))

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