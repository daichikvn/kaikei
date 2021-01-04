from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.db.models import Sum
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .forms import SalesForm
from .models import Sales
import calendar
import datetime
from .lib import setDateTime, setData, setGraph

@login_required
def index(request):
    category_dict = {}
    matrix_list = []
    past_matrix_list = []
    day_matrix_list = []
    past_day_matrix_list = []


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


    month_data = setData.setMonthSales(request, this_year, this_month)
    total = setData.getTotalSales(month_data)
    drink = setData.getDrinkSales(month_data)
    food = total - drink
    lunch = setData.getLunchSales(month_data)
    dinner = total - lunch
    guest = setData.getGuestSales(month_data)
    average, sales_day = setData.getAverageSales(month_data, total)
    deposit = setData.getDepositSales(month_data)

    """PieChart"""
    category_dict = setGraph.makePieChart(total, food, drink)

    """"BarChart"""
    matrix_list = setGraph.makeBarChart(request, this_year)
    past_matrix_list = setGraph.makeBarChart(request, previous_year)

    day_matrix_list = setGraph.makeDayBarChart(request, this_year, this_month)
    past_day_matrix_list = setGraph.makeDayBarChart(request, previous_year, this_month)

    return render(request, 'sales/index.html',{
        'this_year': this_year,
        'previous_year': previous_year,
        'this_month': this_month,
        'previous_month': previous_month,
        'next_month': next_month,
        'total': total,
        'food': food,
        'drink': drink,
        'lunch': lunch,
        'dinner': dinner,
        'guest': guest,
        'average': average,
        'sales_day': sales_day,
        'deposit': deposit,
        'category_dict': category_dict,
        'matrix_list': matrix_list,
        'past_matrix_list': past_matrix_list,
        'day_matrix_list': day_matrix_list,
        'past_day_matrix_list': past_day_matrix_list,
    })


class SalesListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Sales
    template_name = 'sales/sales_list.html'

    def queryset(self):
        return Sales.objects.filter(author=self.request.user).order_by('-pk')


class SalesCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Sales
    form_class = SalesForm
    success_url = reverse_lazy('sales:create_done')

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(SalesCreateView, self).form_valid(form)

@login_required
def create_done(request):
    return render(request, 'sales/create_done.html')


class SalesUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Sales
    form_class = SalesForm
    success_url = reverse_lazy('sales:update_done')

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(SalesUpdateView, self).form_valid(form)

@login_required
def update_done(request):
    return render(request, 'sales/update_done.html')


class SalesDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Sales
    success_url = reverse_lazy('sales:delete_done')

@login_required
def delete_done(request):
    return render(request, 'sales/delete_done.html')
