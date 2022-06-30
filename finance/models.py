from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class ExpenseItem(models.Model):
    user    = models.ForeignKey(User, verbose_name="投稿者", on_delete=models.CASCADE)
    income  = models.BooleanField(verbose_name="収入")
    name    = models.CharField(verbose_name="費目", max_length=20)

    def __str__(self):
        return self.name


class Balance(models.Model):
    user        = models.ForeignKey(User, verbose_name="投稿者", on_delete=models.CASCADE)
    dt          = models.DateTimeField(verbose_name="投稿日時", default=timezone.now)
    expense_item    = models.ForeignKey(ExpenseItem, verbose_name="費目", on_delete=models.SET_NULL, null=True)

    amount      = models.PositiveIntegerField(verbose_name="金額")
    use_date    = models.DateField(verbose_name="利用日")
    description = models.CharField(verbose_name="利用内容", max_length=100, null=True, blank=True)


"""
class Bank(models.Model):
    user    = models.ForeignKey(User, verbose_name="投稿者", on_delete=models.CASCADE)
    

class Card(models.Model):
    user    = models.ForeignKey(User, verbose_name="投稿者", on_delete=models.CASCADE)


class Deposit(models.Model):
    pass

class CardUsage(models.Model):
    pass

class Payment(models.Model):
    pass
"""

