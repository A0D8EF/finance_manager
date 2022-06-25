from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Balance(models.Model):
    user        = models.ForeignKey(User, verbose_name="投稿者", on_delete=models.CASCADE)
    dt          = models.DateTimeField(verbose_name="投稿日時", default=timezone.now)

    income      = models.BooleanField(verbose_name="収入")
    amount      = models.PositiveIntegerField(verbose_name="金額")
    use_date    = models.DateField(verbose_name="利用日")
    description = models.CharField(verbose_name="利用内容", max_length=100, null=True, blank=True)


"""
class Bank(models.Model):
    user    = models.ForeignKey(User, verbose_name="")



class Card(models.Model):
    pass

class Deposit(models.Model):
    pass

class CardUsage(models.Model):
    pass

class Payment(models.Model):
    pass

class ExpenseItem(models.Model):
    pass

"""

