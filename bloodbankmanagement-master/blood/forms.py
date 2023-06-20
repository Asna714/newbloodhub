from django import forms

from . import models

class BloodForm(forms.ModelForm):
    class Meta:
        model=models.Stock
        fields=['bloodgroup','unit']

class RequestForm(forms.ModelForm):
    class Meta:
        model=models.BloodRequest
        fields=['patient_name','patient_age','reason','bloodgroup','unit']

from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('date', 'address')

    

        


