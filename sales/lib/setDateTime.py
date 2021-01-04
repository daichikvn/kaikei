import datetime


"""今日"""
def nowDate():
    today = datetime.datetime.today()
    year = int(today.strftime("%Y"))
    month = int(today.strftime("%m"))
    return year, month

"""前月"""
def previousMonth(year, month):
    if month == 1:
        year -= 1
        month = 12
    else:
        month -= 1
    return year, month

"""次月"""
def nextMonth(year, month):
    if month == 12:
        year += 1
        month = 1
    else:
        month += 1
    return year, month

"""前月&次月作成"""
def previousAndNextMonthCreation(month):
    if month == 1:
        pre = 12
        nex = month + 1
    elif month == 12:
        pre = month - 1
        nex = 1
    else:
        pre = month - 1
        nex = month + 1
    return pre, nex