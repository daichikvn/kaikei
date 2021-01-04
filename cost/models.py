from django.db import models
from django.contrib.auth.models import User

from datetime import datetime


class Category(models.Model):
    class Meta:
        db_table = "category"
        verbose_name ="カテゴリ"
        verbose_name_plural ="カテゴリ"

    category_name = models.CharField(max_length=255,unique=True)

    def __str__(self):
        return self.category_name


class Shop(models.Model):
    class Meta:
        db_table = "shop"
        verbose_name ="店名"
        verbose_name_plural ="店名"

    shop_name = models.CharField(max_length=255,unique=True)
    flag = models.IntegerField(verbose_name="フラグ")
    category = models.ForeignKey(Category, on_delete = models.PROTECT, verbose_name="カテゴリ")

    def __str__(self):
        return '{0} {1}'.format(self.shop_name, self.flag)


class Cost(models.Model):
    class Meta:
        db_table = "cost"
        verbose_name ="経費"
        verbose_name_plural ="経費"

    date = models.DateField(verbose_name="日付",default=datetime.now)
    shop = models.ForeignKey(Shop, on_delete = models.PROTECT, verbose_name="店名")
    price = models.IntegerField(verbose_name="金額(税込み)", help_text="半角入力")
    memo = models.CharField(verbose_name="備考", max_length=500, blank=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="ユーザー")
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    def __str__(self):
        return '{0} {1} {2}'.format(self.date, self.shop, self.price)
