from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum,Q
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.core.mail import send_mail
from django.contrib.auth.models import User
from blood import forms as bforms
from blood import models as bmodels
from geopy.distance import geodesic
from django.shortcuts import HttpResponse


def donor_signup_view(request):
    userForm=forms.DonorUserForm()
    donorForm=forms.DonorForm()
    mydict={'userForm':userForm,'donorForm':donorForm}
    if request.method=='POST':
        userForm=forms.DonorUserForm(request.POST)
        donorForm=forms.DonorForm(request.POST,request.FILES)
        if userForm.is_valid() and donorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            donor=donorForm.save(commit=False)
            donor.user=user
            donor.bloodgroup=donorForm.cleaned_data['bloodgroup']
            donor.save()
            my_donor_group = Group.objects.get_or_create(name='DONOR')
            my_donor_group[0].user_set.add(user)
        return HttpResponseRedirect('donorlogin')
    return render(request,'donor/donorsignup.html',context=mydict)


from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Donor, BloodDonate

@login_required(login_url='login')
def donor_dashboard_view(request):
    donor = Donor.objects.get(user=request.user)
    approved_donations = BloodDonate.objects.filter(donor=donor, status='Approved').order_by('-date')

    # Calculate last donation date
    if approved_donations.count() > 0:
        last_donation = approved_donations[0].date
    else:
        last_donation = None

    # Calculate next donation date (56 days after last donation date)
    if last_donation:
        next_donation = last_donation + timedelta(days=56)
        today = datetime.today().date()
        can_donate = True if today >= next_donation else False
    else:
        next_donation = None
        can_donate = True  # First-time donors can always donate

    requestmade = BloodDonate.objects.filter(donor=donor).count()
    requestpending = BloodDonate.objects.filter(donor=donor, status='Pending').count()
    requestapproved = BloodDonate.objects.filter(donor=donor, status='Approved').count()
    requestrejected = BloodDonate.objects.filter(donor=donor, status='Rejected').count()

    context = {
        'donor': donor,
        'approved_donations': approved_donations,
        'requestmade': requestmade,
        'requestpending': requestpending,
        'requestapproved': requestapproved,
        'requestrejected': requestrejected,
        'next_donation_date': next_donation,
        'can_donate': can_donate,
    }
    return render(request, 'donor/donor_dashboard.html', context)



def donate_blood_view(request):
    donation_form=forms.DonationForm()
    if request.method=='POST':
        donation_form=forms.DonationForm(request.POST)
        if donation_form.is_valid():
            blood_donate=donation_form.save(commit=False)
            blood_donate.bloodgroup=donation_form.cleaned_data['bloodgroup']
            donor= models.Donor.objects.get(user_id=request.user.id)
            blood_donate.donor=donor
            blood_donate.save()
            return HttpResponseRedirect('donation-history')  
    return render(request,'donor/donate_blood.html',{'donation_form':donation_form})

def donation_history_view(request):
    donor= models.Donor.objects.get(user_id=request.user.id)
    donations=models.BloodDonate.objects.all().filter(donor=donor)
    return render(request,'donor/donation_history.html',{'donations':donations})

def make_request_view(request):
    request_form=bforms.RequestForm()
    if request.method=='POST':
        request_form=bforms.RequestForm(request.POST)
        if request_form.is_valid():
            blood_request=request_form.save(commit=False)
            blood_request.bloodgroup=request_form.cleaned_data['bloodgroup']
            donor= models.Donor.objects.get(user_id=request.user.id)
            blood_request.request_by_donor=donor
            blood_request.save()
            return HttpResponseRedirect('request-history')  
    return render(request,'donor/makerequest.html',{'request_form':request_form})

def request_history_view(request):
    donor= models.Donor.objects.get(user_id=request.user.id)
    blood_request=bmodels.BloodRequest.objects.all().filter(request_by_donor=donor)
    return render(request,'donor/request_history.html',{'blood_request':blood_request})

from .models import Donor


import requests

from django.shortcuts import render


def find_closest_address(request):
    if request.method == 'POST':
        address = request.POST['address']
        blood_group = request.POST['blood_group']

        # Make a request to OpenRouteService API to retrieve latitude and longitude
        api_key = '5b3ce3597851110001cf62486aaf0e18920a4e299c63548ca96ab12d'  # Replace with your actual API key
        geocode_url = f'https://api.openrouteservice.org/geocode/search?api_key={api_key}&text={address}'

        try:
            response = requests.get(geocode_url)
            data = response.json()
            latitude = data['features'][0]['geometry']['coordinates'][1]
            longitude = data['features'][0]['geometry']['coordinates'][0]
        except (requests.RequestException, IndexError, KeyError) as e:
            # Handle the exception accordingly
            return HttpResponse('Error retrieving latitude and longitude')

        user_location = (latitude, longitude)

        # Rest of the code remains the same...
        donors = Donor.objects.filter(bloodgroup=blood_group)
        distances = []
        for donor in donors:
            location = (donor.latitude, donor.longitude)
            distance = geodesic(user_location, location).km
            distances.append((donor, distance))
        distances.sort(key=lambda x: x[1])
        if distances:
            closest_donors = [(donor, distance) for donor, distance in distances]
            context = {'closest_donors': closest_donors}
            return render(request, 'donor/result.html', context)
        else:
            message = 'No donors found.'
            context = {'message': message}
            return render(request, 'donor/indexx.html', context)
    else:
        return render(request, 'donor/indexx.html')
















