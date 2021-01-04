from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Sales


class SalesResource(resources.ModelResource):
    class Meta:
        model = Sales


@admin.register(Sales)
class SalesAdmin(ImportExportModelAdmin):
    ordering = ['id']
    list_display=('id', 'date', 'total_sales', 'lunch_sales', 'drink_sales', 'dinner_guest', 'lunch_guest', 'bank_deposit', 'author')

    resource_class = SalesResource