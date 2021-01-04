from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from cost.models import Category, Shop, Cost
from sales.models import Sales
from .forms import CSVUploadForm

import calendar
import csv
import datetime
import io
import openpyxl
from openpyxl.styles import Border, Side
from openpyxl.styles.fills import PatternFill

from .lib import setDateTime, setData, setGraph, setExcel


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'


@login_required
def index(request):
    sales_matrix_list = []
    cost_matrix_list = []

    if 'param' in request.GET:
        param = request.GET['param']
        this_year = int(request.GET['year'])
        this_month = int(request.GET['month'])
        if param == 'previous':
            this_year, this_month = setDateTime.previousMonth(this_year, this_month)
        elif param == 'next':
            this_year, this_month = setDateTime.nextMonth(this_year, this_month)
        else:
            pass
    else:
        this_year, this_month = setDateTime.nowDate()

    previous_month, next_month = setDateTime.previousAndNextMonthCreation(this_month)
    previous_year = this_year - 1

    gain, cost, sales = setData.getGain(request, this_year, this_month)
    drink_rate = setData.getCostRate(request, this_year, this_month, "ドリンク", None)
    food_rate = setData.getCostRate(request, this_year, this_month, "食材", sales)

    sales_matrix_list = setGraph.makeLineChart(request, this_year, "売上")
    cost_matrix_list = setGraph.makeLineChart(request, this_year, "経費")

    return render(request, 'accounts/index.html',{
        'this_year': this_year,
        'this_month': this_month,
        'previous_month': previous_month,
        'next_month': next_month,
        'gain': gain,
        'food_rate': food_rate,
        'drink_rate': drink_rate,
        'sales_matrix_list': sales_matrix_list,
        'cost_matrix_list': cost_matrix_list,
    })


@login_required
def payment(request):
    today = datetime.datetime.today()
    this_year = today.strftime("%Y")
    return render(request, 'accounts/payment.html',{
        'this_year': this_year,
    })


@login_required
def payment_list(request):
    shop_label_list = [] # 納品店名リストを格納
    shop_monthly_data = {}
    delivery_total = 0

    """date__range"""
    year = request.POST.get('year')
    month = request.POST.get('month')
    month_range = calendar.monthrange(int(year),int(month))[1]
    first_date = str(year) + '-' + str(month) +'-' + '01'
    last_date = str(year) + '-' + str(month) + '-' + str(month_range)
    """Shop_label"""
    Shop_data = Shop.objects.filter(flag=1)
    for i in Shop_data:
        shop_label_list.append((i.shop_name))
        shop_label_list.sort()
    for i in range(len(shop_label_list)):
        shop_monthly_total = Cost.objects.filter(author=request.user, date__year=year, date__month=month, shop__shop_name=shop_label_list[i]).aggregate(sum=models.Sum('price'))['sum']
        if shop_monthly_total != None:
            shop_monthly_data[shop_label_list[i]] = shop_monthly_total
            delivery_total += shop_monthly_total

    return render(request, 'accounts/payment_list.html',{
        'shop_monthly_data': shop_monthly_data,
        'delivery_total': delivery_total,
    })


@login_required
def excel(request):
    today = datetime.datetime.today()
    this_year = today.strftime("%Y")
    return render(request, 'accounts/excel.html',{
        'this_year': this_year,
    })


@login_required
def excel_cost(request):
    year = request.POST.get('cost_year')
    month = request.POST.get('cost_month')
    response = setExcel.makeCostExe(request, year, month)
    return response


@login_required
def excel_delivery(request):
    year = request.POST.get('delivery_year')
    month = request.POST.get('delivery_month')
    response = setExcel.makeDeliveryExe(request, year, month)
    return response


@login_required
def excel_sales(request):
    year = request.POST.get('sales_year')
    month = request.POST.get('sales_month')
    response = setExcel.makeSalesExe(request, year, month)
    return response


@login_required
def excel_rate(request):
    year = request.POST.get('rate_year')
    month = request.POST.get('rate_month')
    response = setExcel.makeRateExe(request, year, month)
    return response


# class PostImport(LoginRequiredMixin, generic.FormView):
#     template_name = 'accounts/import.html'
#     success_url = reverse_lazy('accounts:import')
#     form_class = CSVUploadForm

#     def form_valid(self, form):
#         form.save()
#         return redirect('accounts:import')