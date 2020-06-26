from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='home'),
    path('delete/<city_name>/', views.remove_city,name='remove_city'),
]