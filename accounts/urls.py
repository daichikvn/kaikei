from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('', views.index, name='index'),
    path('payment/', views.payment, name='payment'),
    path('payment_list/', views.payment_list, name='payment_list'),
    path('excel/', views.excel, name='excel'),
    path('excel_cost/', views.excel_cost, name='excel_cost'),
    path('excel_delivery/', views.excel_delivery, name='excel_delivery'),
    path('excel_sales/', views.excel_sales, name='excel_sales'),
    path('excel_rate/', views.excel_rate, name='excel_rate'),
    # path('import/', views.PostImport.as_view(), name='import'),
]