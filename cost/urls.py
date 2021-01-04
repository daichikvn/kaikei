from django.urls import path
from . import views


app_name = 'cost'

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.CostListView.as_view(), name='cost_list'),
    path('create/', views.CostCreateView.as_view(), name='cost_create'),
    path('create_done/', views.create_done, name='create_done'),
    path('update/<int:pk>/', views.CostUpdateView.as_view(), name='cost_update'),
    path('update_done/', views.update_done, name='update_done'),
    path('delete/<int:pk>/', views.CostDeleteView.as_view(), name='cost_delete'),
    path('delete_done/', views.delete_done, name='delete_done'),
]