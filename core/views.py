from django.shortcuts import render
from django.views import View
from . models import Measurement, Sensor
from django.db.models import F, Q
from django_admin_geomap import geomap_context
from PIL import Image
from PIL import ImageDraw
import os
from django.conf import settings
from plotly.offline import plot
from plotly.graph_objs import Scatter


class TableView(View):
    def get_data(self, process):
        if process == 'none':
            entries = Measurement.objects.all()
        elif process == 'sensor':
            entries = Measurement.objects.all().order_by('s_id')
        elif process == 'time_inc':
            entries = Measurement.objects.all().order_by('m_timestamp')
        elif process == 'time_dec':
            entries = Measurement.objects.all().order_by('-m_timestamp')
        elif process == 'err_value':
            entries = Measurement.objects.all().filter(Q(m_value__gte=F('s_id__st_id__st_high_value')) | Q(m_value__lte=F('s_id__st_id__st_low_value')))
        else:
            entries = Measurement.objects.all()

        return entries

    def get(self, request):
        process = request.session.get('proc', 'none')
        
        context = {
            'entries': self.get_data(process),
            'process': process
        }

        return render(request, 'table.html', context)

    def post(self, request):
        process = request.POST.get('process')
        
        request.session['proc'] = process

        context = {
            'entries': self.get_data(process),
            'process': process
        }

        return render(request, 'table.html', context)


class MapView(View):
    def get(self, request):
        sensors = Sensor.objects.all()

        for sensor in sensors:
            sensor_meas = Measurement.objects.filter(s_id=sensor.s_id).last().m_value
            sensor_type = sensor.st_id.st_name
            if sensor_type == 'CO sensor':
                sensor_type = 'CO'
            elif sensor_type == 'Temperature sensor':
                sensor_type = 'Temp'
            elif sensor_type == 'Wind sensor':
                sensor_type = 'Wind'
            message = f'<span><strong>{sensor_type}:</strong> {sensor_meas:.2f} <em>{sensor.st_id.st_unit}</em></span>'
            sensor.default_popup_message = message            
            
        return render(request, 'map.html', geomap_context(sensors, auto_zoom='13'))


class GraphView(View):
    def get(self, request):
        sensors = Sensor.objects.all()
        scatters = list()

        for sensor in sensors:
            measurements = Measurement.objects.filter(s_id=sensor.s_id)
            x_data = [meas.m_timestamp for meas in measurements]
            y_data = [meas.m_value for meas in measurements]
            line_name = f'{sensor.st_id.st_name} ({sensor.s_name})'
            scatter = Scatter(x=x_data, y=y_data, mode='lines+markers', name=line_name, opacity=0.8)
            scatters.append(scatter)

        plot_div = plot(scatters, output_type='div')
        
        context = {
            'plot_div': plot_div
        }

        return render(request, 'graph.html', context)

