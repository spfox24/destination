from django.forms import ModelForm
from .models import Itinerary

class ItineraryForm(ModelForm):
  class Meta:
    model = Itinerary
    fields = ['date', 'activity']
