from django.db import models
from django.db.models import Sum
from ..models import Sales
import calendar


"""円グラフ"""
def makePieChart(total, food, drink):
    category_dict = {} # カテゴリ毎の割合を格納する
    if total != 0:
        food_ratio = int((food / total) *100)
        category_dict.setdefault("フード", food_ratio)
        drink_ratio = int((drink / total) *100)
        category_dict.setdefault("ドリンク", drink_ratio)
    return category_dict

"""棒グラフ"""
def makeBarChart(request, year):
    dateList = []
    monthlyTotalData = []
    matrixList = []

    data = Sales.objects.filter(author=request.user, date__year=year)
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
        monthData = Sales.objects.filter(author=request.user, date__range=(first_date, last_date)).aggregate(sum=models.Sum('total_sales'))['sum']
        monthlyTotalData.append([xLabel[i], monthData])
    for i in range(12):
        i = str(i + 1)
        matrixList.append([str(year) + "/" + i.zfill(2), 0])
    for yyyy_mm, total in monthlyTotalData:
        for i, data in enumerate(matrixList):
            if data[0] == yyyy_mm:
                matrixList[i][1] = total
    return matrixList

def makeDayBarChart(request, year, month):
    dateDayList = []
    monthlyDayData = []
    dayMatrixList = []

    data = Sales.objects.filter(author=request.user, date__year=year, date__month=month)
    for i in data:
        dateDayList.append((i.date.strftime('%Y/%m/%d')[8:]))
        dateDayList.sort()
    xDayLabel = list(set(dateDayList))
    xDayLabel.sort(reverse=False)
    for i in range(len(xDayLabel)):
        dayData = Sales.objects.get(author=request.user, date__year=year, date__month=month, date__day=xDayLabel[i])
        monthlyDayData.append([xDayLabel[i], dayData.total_sales])
    for i in range(31):
        i = str(i + 1)
        dayMatrixList.append([i.zfill(2), 0])
    for day, price in monthlyDayData:
        for i, data in enumerate(dayMatrixList):
            if data[0] == day:
                dayMatrixList[i][1] = price
    return dayMatrixList