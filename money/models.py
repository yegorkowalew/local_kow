from django.db import models
from django.utils import timezone

# Create your models here.

class Post(models.Model):
#    author = models.ForeignKey('auth.User')
#    title = models.CharField(max_length=200)
    money = models.FloatField()
    created_date = models.DateTimeField(
            default=timezone.now)
#    published_date = models.DateTimeField(
#            blank=True, null=True)

#    def publish(self):
#        self.published_date = timezone.now()
#        self.save()

    def __str__(self):
        return str(self.created_date)

class Tarif(models.Model):
    money_for_mons = models.PositiveIntegerField(default=200)

    def __str__(self):
        return str(self.money_for_mons)

