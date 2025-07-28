# weather/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('provinces/', views.get_provinces),
    path('districts/', views.get_districts),
    path('wards/', views.get_wards),
    path('weather/', views.get_weather_by_ward),
    path('hydrology/', views.get_hydrology_data),  # ✅ mới thêm
    path('stations/', views.get_stations),

]



