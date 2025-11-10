from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_accident, name='add_accident'),
    path('map/', views.map_view, name='map_view'),
    path('search/', views.search_accidents, name='search_accidents'),
    path('statistics/', views.statistics, name='statistics'),
    path('filter/', views.filter_accidents, name='filter_accidents'),
    
]