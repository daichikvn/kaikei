from django.db import models
from django.db.models import Sum
from cost.models import Category, Shop, Cost
from sales.models import Sales
import calendar


"""折線グラフ"""
def makeLineChart(request, year, flag):
    dateList = []
    monthlyTotalData = []
    matrixList = []
    if flag == "売上":
        data = Sales.objects.filter(author=request.user, date__year=year)
    elif flag == "経費":
        data = Cost.objects.filter(author=request.user, date__year=year)
    for i in data:
        dateList.append((i.date.strftime('%Y/%m/%d')[:7]))
        dateList.sort()
    xLabel = list(set(dateList))
    xLabel.sort(reverse=False)
    for i in range(len(xLabel)):
        y, m = xLabel[i].split("/")
        month_range = calendar.monthrange(int(y),int(m))[1]
        first_date = y + '-' + m +'-' + '01'
        last_date = y + '-' + m + '-' + str(month_range)
        if flag == "売上":
            monthData = Sales.objects.filter(author=request.user, date__range=(first_date, last_date)).aggregate(sum=models.Sum('total_sales'))['sum']
        elif flag == "経費":
            monthData = Cost.objects.filter(author=request.user, date__range=(first_date, last_date)).aggregate(sum=models.Sum('price'))['sum']
        monthlyTotalData.append([xLabel[i], monthData])
    for i in range(12):
        i = str(i + 1)
        matrixList.append([str(year) + "/" + i.zfill(2), 0])
    for yyyy_mm, total in monthlyTotalData:
        for i, data in enumerate(matrixList):
            if data[0] == yyyy_mm:
                matrixList[i][1] = total
    return matrixList