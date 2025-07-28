# weather/models.py
from django.db import models

class Province(models.Model):
    province_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'provinces'

    def __str__(self):
        return self.name

class District(models.Model):
    district_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, db_column='province_id')

    class Meta:
        db_table = 'districts'

    def __str__(self):
        return self.name

class Ward(models.Model):
    ward_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE, db_column='district_id')

    class Meta:
        db_table = 'wards'

    def __str__(self):
        return self.name

class Location(models.Model):
    location_id = models.IntegerField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    ward = models.OneToOneField(Ward, on_delete=models.CASCADE, db_column='ward_id')

    class Meta:
        db_table = 'locations'

    def __str__(self):
        return f"{self.latitude}, {self.longitude}"


# ✅ Sửa: Đưa ra ngoài
class HydrologyStation(models.Model):
    station_id = models.IntegerField(primary_key=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, db_column='location_id')
    station_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'hydrology_stations'

    def __str__(self):
        return self.station_name


class HydrologyData(models.Model):
    hydrology_id = models.AutoField(primary_key=True)
    station = models.ForeignKey(HydrologyStation, on_delete=models.CASCADE, db_column='station_id')
    water_level = models.FloatField()
    measurement_time = models.DateTimeField()

    class Meta:
        db_table = 'hydrology_data'
