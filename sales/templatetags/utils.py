from django import template


register = template.Library()

# 総売上 - ランチ(売上)
# 総売上 - ドリンク(売上)
@register.filter(name="subtraction")
def subtraction(value, args):
    return int(value - args)

# ドリンク(売上) * 100 / 総売上
@register.filter(name="division")
def division(value, args):
    if value == 0 or args == 0:
        return int(0)
    return int(value / args)

def percent(var,args):
    return int(var * args)
register.filter('percent',percent)

# ディナー(客) + ランチ(客)
@register.filter(name="addition")
def addition(value, args):
    return int(value + args)