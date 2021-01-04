import csv
import io
from django import forms
from cost.models import Category, Shop, Cost
from sales.models import Sales


class CSVUploadForm(forms.Form):
    file = forms.FileField(label='CSVファイル', help_text='拡張子csvのファイルをアップロードしてください。')

    def clean_file(self):
        file = self.cleaned_data['file']

        if not file.name.endswith('.csv'):
            raise forms.ValidationError('拡張子がcsvのファイルをアップロードしてください')

        csv_file = io.TextIOWrapper(file, encoding='utf-8')
        reader = csv.reader(csv_file)

        self._instances = []
        try:
            for row in reader:
                # csv_data = Category(pk=row[0], category_name=row[1])
                # csv_data = Shop(pk=row[0], shop_name=row[1], flag=row[2], category_id=row[3])
                # csv_data = Cost(pk=row[0], date=row[1], shop_id=row[2], price=row[3], memo=row[4], author_id=row[5])
                csv_data = Sales(pk=row[0], date=row[1], total_sales=row[2], lunch_sales=row[3], drink_sales=row[4], dinner_guest=row[5], lunch_guest=row[6], author_id=row[7])
                self._instances.append(csv_data)
        except UnicodeDecodeError:
                raise forms.ValidationError('ファイルのエンコーディングや、正しいCSVファイルか確認ください。')

        return file

    def save(self):
        for csv_data in self._instances:
            csv_data.save()
