from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Client, Visit


class ClientResource(resources.ModelResource):
    class Meta:
        model = Client


class VisitResource(resources.ModelResource):
    class Meta:
        model = Visit


@admin.register(Client)
class ClientAdmin(ImportExportModelAdmin):
    ordering = ['id']
    list_display=('id', 'client_name', 'receipt_name', 'memo', 'author')

    resource_class = ClientResource


@admin.register(Visit)
class VisitAdmin(ImportExportModelAdmin):
    ordering = ['id']
    list_display=('id', 'client', 'visit_date', 'menu')

    resource_class = VisitResource