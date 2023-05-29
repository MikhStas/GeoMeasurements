from django.contrib import admin
from .models import *


admin.site.register(Measurement)
admin.site.register(Sensor)
admin.site.register(SensorType)
