from rest_framework import serializers
from .models import Province, District

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['province_id', 'name']

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['district_id', 'name']


# weather/serializers.py
from rest_framework import serializers
from .models import HydrologyData, HydrologyStation

class HydrologyStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HydrologyStation
        fields = ['station_id', 'station_name']

class HydrologyDataSerializer(serializers.ModelSerializer):
    station = HydrologyStationSerializer()

    class Meta:
        model = HydrologyData
        fields = ['hydrology_id', 'water_level', 'measurement_time', 'station']

