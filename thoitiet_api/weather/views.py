from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Province, District, Ward, Location, HydrologyData, HydrologyStation
from .serializers import HydrologyDataSerializer
from django.utils.dateparse import parse_date
import requests
import logging

# Cấu hình logging để hiện ra console giống console.log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


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

    # Reset session nếu có ?reset=true
    if request.GET.get('reset') == 'true':
        request.session.pop('weather_data', None)
        request.session.pop('weather_ward', None)

    # Nếu dữ liệu đã tồn tại trong session
    if request.session.get('weather_data') and request.session.get('weather_ward') == wid:
        logging.info("Lấy dữ liệu thời tiết từ session")
        return Response(request.session['weather_data'])

    try:
        loc = Location.objects.get(ward_id=wid)
        lat = loc.latitude
        lon = loc.longitude

        weather_url = f"{settings.WEATHER_API_URL}?key={settings.WEATHER_API_KEY}&q={lat},{lon}&days=7&aqi=yes&alerts=yes"
        res = requests.get(weather_url)

        logging.info(f"Status Code: {res.status_code}")
        if res.status_code == 200:
            data = res.json()
            logging.info("Dữ liệu từ API thời tiết:")
            logging.info(data.get("forecast", {}))

            # Lưu vào session để tái sử dụng
            request.session['weather_data'] = data
            request.session['weather_ward'] = wid

            return Response(data)
        else:
            return Response({"error": "Không thể lấy dữ liệu thời tiết"}, status=500)

    except Location.DoesNotExist:
        return Response({"error": "Không tìm thấy tọa độ xã"}, status=404)



@api_view(['GET'])
def get_hydrology_data(request):
    date_str = request.GET.get('date')  # Lấy ?date=YYYY-MM-DD
    queryset = HydrologyData.objects.select_related('station')

    if date_str:
        parsed_date = parse_date(date_str)
        if not parsed_date:
            return Response({"error": "Ngày không hợp lệ"}, status=400)
        queryset = queryset.filter(measurement_time__date=parsed_date)

    queryset = queryset.order_by('-measurement_time')[:20]
    serialized = HydrologyDataSerializer(queryset, many=True)
    return Response(serialized.data)


@api_view(['GET'])
def get_stations(request):
    stations = HydrologyStation.objects.all().values('station_id', 'station_name')
    return Response(list(stations))
