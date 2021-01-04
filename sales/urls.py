from django.urls import path
from . import views


app_name = 'sales'

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.SalesListView.as_view(), name='sales_list'),
    path('create/', views.SalesCreateView.as_view(), name='sales_create'),
    path('create_done/', views.create_done, name='create_done'),
    path('update/<int:pk>/', views.SalesUpdateView.as_view(), name='sales_update'),
    path('update_done/', views.update_done, name='update_done'),
    path('delete/<int:pk>/', views.SalesDeleteView.as_view(), name='sales_delete'),
    path('delete_done/', views.delete_done, name='delete_done'),
]