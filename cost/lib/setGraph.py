from django.db import models
from django.db.models import Sum
from ..models import Category, Shop, Cost
import calendar


"""円グラフ"""
def makePieChart(request, year, month, listGroup, total):
    category_dict = {} # カテゴリ毎の割合を格納する
    for i, li in enumerate(listGroup):
        data = Cost.objects.filter(author=request.user, date__year=year, date__month=month, shop__category__category_name=listGroup[i]).aggregate(sum=models.Sum('price'))['sum']
        if data != None:
            ratio = int((data / total) *100)
            category_dict[li] = ratio
        else:
            ratio = 0
            category_dict[li] = ratio
    return category_dict

"""棒グラフ"""
def makeBarChart(request, year):
    date_list = []
    x_label = []
    monthly_total_data = [] # 月毎の経費総額を格納する
    matrix_list =[]

    data = Cost.objects.filter(author=request.user, date__year=year)

    for i in data:
        date_list.append((i.date.strftime('%Y/%m/%d')[:7]))
        date_list.sort()
    x_label = list(set(date_list))
    x_label.sort(reverse=False)

    for i in range(len(x_label)):
        y, m = x_label[i].split("/")
        month_range = calendar.monthrange(int(y),int(m))[1]
        first_date = y + '-' + m +'-' + '01'
        last_date = y + '-' + m + '-' + str(month_range)
        month_total = Cost.objects.filter(author=request.user, date__range=(first_date, last_date)).aggregate(sum=models.Sum('price'))['sum']
        monthly_total_data.append([x_label[i], month_total])

    for i in range(12):
        i = str(i + 1)
        matrix_list.append([str(year) + "/" + i.zfill(2), 0])

    for yyyy_mm, total in monthly_total_data:
        for i,data in enumerate(matrix_list):
            if data[0]==yyyy_mm:
                matrix_list[i][1] = total

    return date_list, x_label, monthly_total_data, matrix_list

"""折線グラフ"""
def makeLineChart(request, x_label, category_list):
    monthly_sum_data =[] # カテゴリー毎の月別データを格納する
    border_color =[] # 折れ線グラフのボーダーカラー色の設定
    background_color =[] # 折れ線グラフのバックグラウンドカラー色の設定
    category_matrix_list =[]  # カテゴリが登録されていない月の合計金額は０にセットする。
    border_color_list=['46, 204, 113, 0.8','241, 196, 15, 0.8','155, 89, 182, 0.8','52, 73, 94, 0.8',\
                        '214, 48, 49, 0.8','230, 126, 34, 0.8','231, 76, 60, 0.8','189, 195, 199, 0.8',\
                        '232, 67, 147, 0.8','26, 188, 156, 0.8','234,210,173, 0.8','52, 152, 219, 0.8',\
                        '149, 165, 166, 0.8','255, 255, 255, 0.8']
    background_color_list=['46, 204, 113, 0.5','241, 196, 15, 0.5','155, 89, 182, 0.5','52, 73, 94, 0.5',\
                            '214, 48, 49, 0.5','230, 126, 34, 0.5','231, 76, 60, 0.5','189, 195, 199, 0.5',\
                            '232, 67, 147, 0.5','26, 188, 156, 0.5','234,210,173, 0.5','52, 152, 219, 0.5',\
                            '149, 165, 166, 0.5','255, 255, 255, 0.5']
    for i in range(len(x_label)):
        y, m = x_label[i].split("/")
        month_range = calendar.monthrange(int(y),int(m))[1]
        first_date = y + '-' + m +'-' + '01'
        last_date = y + '-' + m + '-' + str(month_range)
        month_total = Cost.objects.filter(author=request.user, date__range=(first_date, last_date))
        category_total = month_total.values('shop__category').annotate(total_price=Sum('price'))
        for j in range(len(category_total)):
            price = category_total[j]['total_price']
            category = Category.objects.get(pk=category_total[j]['shop__category'])
            monthly_sum_data.append([x_label[i], category.category_name, price])
    for item_label in x_label:
        for item_category in category_list:
            category_matrix_list.append([item_label, item_category, 0])
    for yyyy_mm, category, total in monthly_sum_data:
        for i, data in enumerate(category_matrix_list):
            if data[0] == yyyy_mm and data[1] == category:
                category_matrix_list[i][2] = total
    for x, y in zip(category_list, border_color_list):
        border_color.append([x,y])
    for x, y in zip(category_list, background_color_list):
        background_color.append([x,y])
    return category_matrix_list, border_color, background_color