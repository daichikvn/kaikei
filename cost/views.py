from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.db.models import Sum
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .forms import CostForm
from .models import Category, Shop, Cost
import calendar
import datetime
from .lib import setDateTime, setData, setGraph


@login_required
def index(request):
    date_list = []
    past_date_list = []
    x_label = []
    monthly_total_data = []
    past_monthly_total_data = []
    matrix_list =[]
    past_matrix_list =[]

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

    total = setData.getTotalCost(request, this_year, this_month)
    food = setData.getCategoryCost(request, this_year, this_month, '食材')
    drink = setData.getCategoryCost(request, this_year, this_month, 'ドリンク')
    other = total - (food + drink) # その他
    cash = setData.getFlagCost(request, this_year, this_month, 0)
    cash_food = setData.getFlagCategoryCost(request, this_year, this_month, 0, '食材')
    delivery = setData.getFlagCost(request, this_year, this_month, 1)
    delivery_food = setData.getFlagCategoryCost(request, this_year, this_month, 1, '食材')

    """PieChart"""
    category_list = setData.getCategoryList()
    category_dict = setGraph.makePieChart(request, this_year, this_month, category_list, total)

    """"BarChart"""
    date_list, x_label, monthly_total_data, matrix_list = setGraph.makeBarChart(request, this_year)
    past_date_list, past_x_label, past_monthly_total_data, past_matrix_list = setGraph.makeBarChart(request, previous_year)

    """LineChart"""
    category_matrix_list, border_color, background_color = setGraph.makeLineChart(request, x_label, category_list)

    return render(request, 'cost/index.html',{
        'this_year': this_year,
        'previous_year': previous_year,
        'this_month': this_month,
        'previous_month': previous_month,
        'next_month': next_month,
        'total': total,
        'food': food,
        'drink': drink,
        'other': other,
        'cash': cash,
        'cash_food': cash_food,
        'delivery': delivery,
        'delivery_food': delivery_food,
        'category_list': category_list,
        'category_dict': category_dict,
        'matrix_list': matrix_list,
        'past_matrix_list': past_matrix_list,
        'x_label': x_label,
        'category_matrix_list': category_matrix_list,
        'border_color': border_color,
        'background_color': background_color,
    })


class CostListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Cost
    template_name = 'cost/cost_list.html'

    def queryset(self):
        if 'param' in self.request.GET:
            param = self.request.GET['param']
            this_year = int(self.request.GET['year'])
            this_month = int(self.request.GET['month'])
        return Cost.objects.filter(author=self.request.user, date__year=this_year, date__month=this_month).order_by('-pk')


class CostCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Cost
    form_class = CostForm
    success_url = reverse_lazy('cost:create_done')

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(CostCreateView, self).form_valid(form)

@login_required
def create_done(request):
    return render(request, 'cost/create_done.html')


class CostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Cost
    form_class = CostForm
    success_url = reverse_lazy('cost:update_done')

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(CostUpdateView, self).form_valid(form)

@login_required
def update_done(request):
    return render(request, 'cost/update_done.html')


class CostDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Cost
    success_url = reverse_lazy('cost:delete_done')

@login_required
def delete_done(request):
    return render(request, 'cost/delete_done.html')
