from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('trips/', views.trips_index, name='trips_index'),
    path('trips/<int:trip_id>/', views.trips_detail, name='detail'),
    path('trips/create/', views.TripCreate.as_view(), name='trips_create'),
    path('flight_search/', views.flight_search, name='flight_search'),

    path('accounts/signup/', views.signup, name='signup')
]