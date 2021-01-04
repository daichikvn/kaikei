from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Category, Shop, Cost


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category


class ShopResource(resources.ModelResource):
    class Meta:
        model = Shop


class CostResource(resources.ModelResource):
    class Meta:
        model = Cost


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    ordering = ['id']
    list_display=('id', 'category_name')

    resource_class = CategoryResource


@admin.register(Shop)
class ShopAdmin(ImportExportModelAdmin):
    ordering = ['id']
    list_display=('id', 'shop_name', 'flag', 'category')

    resource_class = ShopResource


@admin.register(Cost)
class CostAdmin(ImportExportModelAdmin):
    ordering = ['id']
    list_display=('id', 'date', 'shop', 'price', 'memo', 'author')

    resource_class = CostResource
