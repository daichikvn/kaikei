from django.urls import path
from . import views


app_name = 'client'

urlpatterns = [
    # path('', views.index, name='index'),
    path('list/', views.ClientListView.as_view(), name='client_list'),
    path('detail/<int:pk>/', views.ClientDetailView.as_view(), name='client_detail'),
    path('create/', views.ClientCreateView.as_view(), name='client_create'),
    path('create_done/', views.create_done, name='create_done'),
    path('create_visit/<int:pk>/', views.create_visit, name='create_visit'),
    path('update/<int:pk>/', views.ClientUpdateView.as_view(), name='client_update'),
    path('update_done/', views.update_done, name='update_done'),
    path('update_visit/<int:pk>/', views.update_visit, name='update_visit'),
    path('delete/<int:pk>/', views.ClientDeleteView.as_view(), name='client_delete'),
    path('delete_done/', views.delete_done, name='delete_done'),
    path('delete_visit/<int:pk>/', views.delete_visit, name='delete_visit'),
]