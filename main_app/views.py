from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Trip

def home(request):
    return render(request, 'home.html')

def trips_index(request):
    trips = Trip.objects.all()
    return render(request, 'trips/index.html', { 'trips': trips })

def trips_detail(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    return render(request, 'trips/detail.html', { 'trip': trip })

class TripCreate(CreateView):
	model = Trip
	fields = ['destination', 'depart', 'arrive', 'hotel', 'budget', 'description']


