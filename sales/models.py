from django.db import models
from django.contrib.auth.models import User

from datetime import datetime


class Sales(models.Model):
    class Meta:
        db_table = "sales"
        verbose_name ="売上"
        verbose_name_plural ="売上"

    date = models.DateField(verbose_name="日付",default=datetime.now)
    total_sales = models.IntegerField(verbose_name="総売上", help_text="半角入力")
    lunch_sales = models.IntegerField(verbose_name="ランチ売上", help_text="半角入力", blank=True, default=0)
    drink_sales = models.IntegerField(verbose_name="ドリンク売上", help_text="半角入力")
    dinner_guest = models.IntegerField(verbose_name="ディナー客", help_text="半角入力")
    lunch_guest = models.IntegerField(verbose_name="ランチ客", help_text="半角入力", blank=True, default=0)
    bank_deposit = models.IntegerField(verbose_name="銀行入金額", help_text="半角入力", blank=True, default=0)
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="ユーザー")
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    def __str__(self):
        return '{0} {1}'.format(self.date, self.total_sales)
