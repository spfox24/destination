from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

class Friend(models.Model):
	name = models.CharField(max_length=100)
	relationship = models.CharField(max_length=100)
	birthdate = models.DateField()

	user = models.ForeignKey(User, on_delete=models.CASCADE)  
	
	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('friends_detail', kwargs={'friend_id': self.id})

class Trip(models.Model):
	destination = models.CharField(max_length=100)
	depart = models.DateField('departure date')
	arrive = models.DateField('return date')
	hotel = models.CharField(max_length=100)
	budget = models.IntegerField()
	description = models.TextField(max_length=250)

	friends = models.ManyToManyField(Friend)

	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.destination

	def get_absolute_url(self):
		return reverse('trips_index')

class Itinerary(models.Model):
	date = models.DateField('Activity Date')
	activity = models.CharField(max_length=100)
	
	trip = models.ForeignKey(Trip, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.activity} on {self.date}"

	def get_absolute_url(self):
		return reverse('trips_index')

class Photo(models.Model):
	url = models.CharField(max_length=250)
	trip = models.ForeignKey(Trip, on_delete=models.CASCADE)

	def __str__(self):
		return f"Photo for trip_id: {self.trip_id} @{self.url}"

