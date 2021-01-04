from django.db import models
from django.contrib.auth.models import User

from datetime import datetime


class Client(models.Model):
    class Meta:
        db_table ="client"
        verbose_name ="顧客"
        verbose_name_plural ="顧客"

    client_name = models.CharField(verbose_name="顧客名", max_length=255)
    receipt_name = models.TextField(verbose_name="領収書宛名", max_length=1000, blank=True)
    tel_number = models.CharField(verbose_name='電話番号', max_length=15, blank=True, help_text="任意 (例: 09012345678)")
    memo = models.TextField(verbose_name="備考", max_length=1000, blank=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="ユーザー")

    def __str__(self):
        return '{0}'.format(self.client_name)


class Visit(models.Model):
    class Meta:
        db_table ="visit"
        verbose_name ="来店記録"
        verbose_name_plural ="来店記録"

    client = models.ForeignKey(Client, related_name='visits', on_delete = models.PROTECT, verbose_name="顧客名")
    visit_date = models.DateField(verbose_name="来店日",default=datetime.now)
    menu = models.TextField(verbose_name="メニュー", max_length=1000, blank=True)
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    def __str__(self):
        return '{0} {1} {2}'.format(self.client, self.visit_date, self.menu)