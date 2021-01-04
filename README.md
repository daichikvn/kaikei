# DB DESIGN

## User
|Column|FieldType|Options|
|------|----|-------|
|pk|AutoField|auto_created=True, primary_key=True, serialize=False|
|username|CharField||
|password|PasswordField||

## Category
|Column|FieldType|Options|
|------|----|-------|
|pk|AutoField|auto_created=True, primary_key=True, serialize=False|
|category_name|CharField|max_length=255, unique=True|

## Shop
|Column|FieldType|Options|
|------|----|-------|
|pk|AutoField|auto_created=True, primary_key=True, serialize=False|
|shop_name|CharField|max_length=255,unique=True|
|flag|IntegerField|verbose_name="フラグ"|
|category|ForeignKey|Category, on_delete = models.PROTECT, verbose_name="カテゴリ"|

## Cost
|Column|FieldType|Options|
|------|----|-------|
|pk|AutoField|auto_created=True, primary_key=True, serialize=False|
|date|DateField|default=datetime.now, verbose_name="日付"|
|shop|ForeignKey|Shop, on_delete = models.PROTECT, verbose_name="店名"|
|price|IntegerField|help_text="半角入力", verbose_name="金額"|
|memo|CharField|max_length=500, blank=True, verbose_name="備考"|
|author|ForeignKey|User, on_delete=models.PROTECT, verbose_name="ユーザー"|
|created_at|DateTimeField|auto_now_add=True, verbose_name='登録日時'|
|updated_at|DateTimeField|auto_now=True, verbose_name='更新日時'|

## Sales
|Column|FieldType|Options|
|------|----|-------|
|pk|AutoField|auto_created=True, primary_key=True, serialize=False|
|date|DateField|default=datetime.now, verbose_name="日付"|
|total_sales|IntegerField|help_text="半角入力", verbose_name="総売上"|
|lunch_sales|IntegerField|help_text="半角入力", blank=True, default=0, verbose_name="ランチ売上"|
|drink_sales|IntegerField|help_text="半角入力", verbose_name="ドリンク売上"|
|dinner_guest|IntegerField|help_text="半角入力", verbose_name="ディナー客"|
|lunch_guest|IntegerField|help_text="半角入力", blank=True, default=0, verbose_name="ランチ客"|
|author|ForeignKey|User, on_delete=models.PROTECT, verbose_name="ユーザー"|
|created_at|DateTimeField|auto_now_add=True, verbose_name='登録日時'|
|updated_at|DateTimeField|auto_now=True, verbose_name='更新日時'|

## Client
|Column|FieldType|Options|
|------|----|-------|
|pk|AutoField|auto_created=True, primary_key=True, serialize=False|
|client_name|CharField|max_length=255, unique=True, verbose_name="顧客名"|
|receipt_name|CharField|max_length=500, blank=True, verbose_name="領収書宛名"|
|memo|TextField|max_length=1000, blank=True, verbose_name="備考"|
|author|ForeignKey|User, on_delete=models.PROTECT, verbose_name="ユーザー"|

## Visit
|Column|FieldType|Options|
|------|----|-------|
|pk|AutoField|auto_created=True, primary_key=True, serialize=False|
|client|ForeignKey|Client, related_name='visits', on_delete = models.PROTECT, verbose_name="顧客名"|
|visit_date|CharField|default=datetime.now, verbose_name="来店日"|
|menu|TextField|max_length=1000, blank=True, verbose_name="メニュー"|
|created_at|DateTimeField|auto_now_add=True, verbose_name='登録日時'|
|updated_at|DateTimeField|auto_now=True, verbose_name='更新日時'|