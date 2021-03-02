import os
import json
from dotenv import find_dotenv, load_dotenv
from amadeus import Client, ResponseError, Location
from django.contrib import messages
from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Trip, Friend

load_dotenv(find_dotenv())

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

amadeus = Client(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, log_level='debug')

def flight_search(request):
    if request.method == 'POST':
        kwargs = {'originCityCode': request.POST.get('Origin'), 
            'period': '2018-03'}

        try:
            results = amadeus.travel.analytics.air_traffic.traveled.get(
                **kwargs).data
        except ResponseError as error:
            print(error)
            messages.add_message(request, messages.ERROR, error)
            return render(request, 'flight_search.html', {})
        return render(request, 'flight_search.html', {'results': results})
    else:
        return render(request, 'flight_search.html', {})

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

class FriendCreate(CreateView):
  model = Friend
  fields = '__all__'
