from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Province, District, Ward, Location
import requests

@api_view(['GET'])
def get_provinces(request):
    data = list(Province.objects.values('province_id', 'name'))
    return Response(data)

@api_view(['GET'])
def get_districts(request):
    pid = request.GET.get('province_id')
    data = list(District.objects.filter(province_id=pid).values('district_id', 'name'))
    return Response(data)

@api_view(['GET'])
def get_wards(request):
    did = request.GET.get('district_id')
    data = list(Ward.objects.filter(district_id=did).values('ward_id', 'name'))
    return Response(data)

@api_view(['GET'])
def get_weather_by_ward(request):
    wid = request.GET.get('ward_id')
    try:
        loc = Location.objects.get(ward_id=wid)
        lat = loc.latitude
        lon = loc.longitude
        weather_url = f"https://api.weatherapi.com/v1/forecast.json?key=cc35923bbac44d40a5b44329252105&q={lat},{lon}&days=1&aqi=yes&alerts=yes"
        res = requests.get(weather_url)
        if res.status_code == 200:
            return Response(res.json())
        else:
            return Response({"error": "Không thể lấy dữ liệu thời tiết"}, status=500)
    except Location.DoesNotExist:
        return Response({"error": "Không tìm thấy tọa độ xã"}, status=404)
    
    # weather/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import HydrologyData
from .serializers import HydrologyDataSerializer
from django.utils.dateparse import parse_date

@api_view(['GET'])
def get_hydrology_data(request):
    date_str = request.GET.get('date')  # Lấy ?date=YYYY-MM-DD
    queryset = HydrologyData.objects.select_related('station')

    if date_str:
        parsed_date = parse_date(date_str)
        if not parsed_date:
            return Response({"error": "Ngày không hợp lệ"}, status=400)
        queryset = queryset.filter(measurement_time__date=parsed_date)

    queryset = queryset.order_by('-measurement_time')[:20]  # Lấy mới nhất
    serialized = HydrologyDataSerializer(queryset, many=True)
    return Response(serialized.data)
@api_view(['GET'])
def get_stations(request):
    from .models import HydrologyStation
    stations = HydrologyStation.objects.all().values('station_id', 'station_name')
    return Response(list(stations))
