from ..models import Sales


"""売上月別データ"""
def setMonthSales(request, year, month):
    data = Sales.objects.filter(author=request.user, date__year=year, date__month=month)
    return data

"""売上総額/月"""
def getTotalSales(data):
    total = 0
    for s in data:
        total += s.total_sales
    return total

"""ドリンク総額/月"""
def getDrinkSales(data):
    drink = 0
    for s in data:
        drink += s.drink_sales
    return drink

"""ランチ総額/月"""
def getLunchSales(data):
    lunch = 0
    for s in data:
        lunch += s.lunch_sales
    return lunch

"""入客数/月"""
def getGuestSales(data):
    guest = 0
    for s in data:
        guest += s.dinner_guest
        guest += s.lunch_guest
    return guest

"""一日平均/営業日数"""
def getAverageSales(data, total):
    average = 0
    sales_day = 0
    if len(data) != 0:
        average = round(total / len(data), 2)
        sales_day = len(data)
    return average, sales_day

"""銀行入金額"""
def getDepositSales(data):
    deposit = 0
    for s in data:
        deposit += s.bank_deposit
    return deposit