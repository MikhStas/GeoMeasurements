# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django_admin_geomap import GeoItem


class Measurement(models.Model):
    m_id = models.AutoField(primary_key=True)
    m_value = models.FloatField()
    m_timestamp = models.DateTimeField()
    s_id = models.ForeignKey('Sensor', on_delete=models.CASCADE, db_column='s_id')

    class Meta:
        db_table = 'Measurement'


class Sensor(models.Model, GeoItem):
    s_id = models.AutoField(primary_key=True)
    s_date = models.DateField(blank=True, null=True)
    s_name = models.CharField(max_length=100)
    s_lat = models.FloatField()
    s_long = models.FloatField()
    st_id = models.ForeignKey('SensorType', on_delete=models.CASCADE, db_column='st_id')

    class Meta:
        db_table = 'Sensor'

    @property
    def geomap_longitude(self):
        return '' if self.s_long is None else str(self.s_long)

    @property
    def geomap_latitude(self):
        return '' if self.s_lat is None else str(self.s_lat)


class SensorType(models.Model):
    st_id = models.AutoField(primary_key=True)
    st_name = models.CharField(max_length=50)
    st_high_value = models.FloatField(blank=True, null=True)
    st_low_value = models.FloatField(blank=True, null=True)
    st_unit = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'Sensor_type'
