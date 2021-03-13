import os
import json
import uuid
import boto3
from dotenv import find_dotenv, load_dotenv
from amadeus import Client, ResponseError, Location
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Trip, Photo, Itinerary, Friend
from .forms import ItineraryForm

load_dotenv(find_dotenv())

S3_BASE_URL = 'https://s3-us-east-2.amazonaws.com/'
BUCKET = 'destination-app'

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

def signup(request):
    error_message = ''

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid data for sign up.'

    form = UserCreationForm()
    context = { 'form': form, 'error_message': error_message }
    return render(request, 'registration/signup.html', context)

@login_required
def add_photo(request, trip_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]

        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, trip_id=trip_id)
            photo.save()
        except:
            print('An error has occured uploading file')
    return redirect('detail', trip_id=trip_id)

amadeus = Client(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, log_level='debug')

@login_required
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

@login_required
def trips_index(request):
    trips = Trip.objects.filter(user=request.user)
    return render(request, 'trips/index.html', { 'trips': trips })

@login_required
def trips_detail(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    friends_trip_doesnt_have = Friend.objects.exclude(id__in = trip.friends.all().values_list('id'))
    itinerary_form = ItineraryForm()
    return render(request, 'trips/detail.html', {
        'trip': trip, 
        'itinerary_form': itinerary_form,
        'friends': friends_trip_doesnt_have
        })

@login_required
def add_itinerary(request, trip_id):
    form = ItineraryForm(request.POST)
    if form.is_valid():
        new_itinerary = form.save(commit=False)
        new_itinerary.trip_id = trip_id
        new_itinerary.save()
    return redirect('detail', trip_id=trip_id)

@login_required
def remove_itinerary(request, pk):
    itinerary = get_object_or_404(Itinerary, pk=pk)
    itinerary.delete()
    trips = Trip.objects.filter(user=request.user)
    return redirect('/trips/', { 'trips': trips })

@login_required
def friends_index(request):
    friends = Friend.objects.filter(user=request.user)
    return render(request, 'friends/index.html', { 'friends': friends })

@login_required
def friends_detail(request, friend_id):
    friend = Friend.objects.get(id=friend_id)
    return render(request, 'friends/detail.html', { 'friend': friend })

@login_required
def assoc_friend(request, trip_id, friend_id):
    Trip.objects.get(id=trip_id).friends.add(friend_id)
    return redirect('detail', trip_id=trip_id)

@login_required
def remove_friend(request, trip_id, friend_id):
    Trip.objects.get(id=trip_id).friends.remove(friend_id)
    return redirect('detail', trip_id=trip_id)

class TripCreate(LoginRequiredMixin, CreateView):
    model = Trip
    fields = ['destination', 'depart', 'arrive', 'hotel', 'budget', 'description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TripDelete(LoginRequiredMixin, DeleteView):
    model = Trip
    success_url = '/trips/'


class TripUpdate(LoginRequiredMixin, UpdateView):
    model = Trip
    fields = ['destination', 'depart', 'arrive', 'hotel', 'budget', 'description']


class FriendCreate(LoginRequiredMixin, CreateView):
    model = Friend
    fields = ['name', 'relationship', 'birthdate']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class FriendUpdate(LoginRequiredMixin, UpdateView):
    model = Friend
    fields = ['name', 'relationship', 'birthdate']

class FriendDelete(LoginRequiredMixin, DeleteView):
    model = Friend
    success_url = '/friends/'
