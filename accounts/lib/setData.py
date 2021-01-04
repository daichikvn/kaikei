from cost.models import Category, Shop, Cost
from sales.models import Sales


"""利益/月"""
def getGain(request, year, month):
    cost = 0
    sales = 0
    costData = Cost.objects.filter(author=request.user, date__year=year, date__month=month)
    for c in costData:
        cost += c.price
    salesData = Sales.objects.filter(author=request.user, date__year=year, date__month=month)
    for s in salesData:
        sales += s.total_sales
    gain = sales - cost
    return gain, cost, sales

"""原価率/月"""
def getCostRate(request, year, month, category, sales_total):
    cost = 0
    sales = 0
    rate = 0
    costData = Cost.objects.filter(author=request.user, date__year=year, date__month=month, shop__category__category_name=category)
    for c in  costData:
        cost += c.price
    if category == "ドリンク":
        salesData = Sales.objects.filter(author=request.user, date__year=year, date__month=month)
        for s in salesData:
            sales += s.drink_sales
    elif category == "食材":
        salesData = Sales.objects.filter(author=request.user, date__year=year, date__month=month)
        for s in salesData:
            sales += s.drink_sales
        sales = sales_total - sales
    if sales != 0:
        rate = round(cost / sales * 100, 2)
    return rate