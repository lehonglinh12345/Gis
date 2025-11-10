from django.urls import path
from . import views

urlpatterns = [
    # Trang Dashboard chính (sử dụng name='index' để khớp với base.html)
    path('', views.dashboard, name='index'), 
    
    # Xử lý thêm tai nạn (form trên dashboard sẽ POST đến đây)
    path('add/', views.add_accident, name='add_accident'),
    path('api/geojson/province/', views.api_get_geojson_by_province, name='api_get_geojson_by_province'),
    # --- CÁC API ENDPOINT MỚI ---
    path('api/accidents/', views.api_get_accidents, name='api_get_accidents'),
    path('api/statistics/', views.api_get_statistics, name='api_get_statistics'),
    

]