from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('trips/', views.trips_index, name='trips_index'),
    path('trips/<int:trips_id>/', views.trips_detail, name='trips_detail'),
    path('trips/create/', views.TripCreate.as_view(), name='trips_create'),
]