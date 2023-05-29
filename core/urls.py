from django.urls import path
from . import views


urlpatterns = [
    path('', views.MapView.as_view()),
    path('table/', views.TableView.as_view()),
    path('map/', views.MapView.as_view()),
    path('graph/', views.GraphView.as_view()),
]
