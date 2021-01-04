from ..models import Category, Shop, Cost


"""経費総額/月"""
def getTotalCost(request, year, month):
    cost = 0
    data = Cost.objects.filter(author=request.user, date__year=year, date__month=month)
    for c in data:
        cost += c.price
    return cost

"""カテゴリ総額/月"""
def getCategoryCost(request, year, month, category):
    cost = 0
    data = Cost.objects.filter(author=request.user, date__year=year, date__month=month, shop__category__category_name=category)
    for c in data:
        cost += c.price
    return cost

"""フラグ総額/月"""
def getFlagCost(request, year, month, flag):
    cost = 0
    data = Cost.objects.filter(author=request.user, date__year=year, date__month=month, shop__flag=flag)
    for c in data:
        cost += c.price
    return cost

"""フラグ毎カテゴリ総額/月"""
def getFlagCategoryCost(request, year, month, flag, category):
    cost = 0
    data = Cost.objects.filter(author=request.user, date__year=year, date__month=month, shop__category__category_name=category, shop__flag=flag)
    for c in data:
        cost += c.price
    return cost

"""カテゴリリスト"""
def getCategoryList():
    category_list = []
    data = Category.objects.all().order_by('-category_name')
    for c in data:
        category_list.append(c.category_name)
    return category_list