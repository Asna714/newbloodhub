from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.shortcuts import render
from .forms import BankForm
from . models import Bank

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import BankForm

def bank_signup_view(request):
    form = BankForm()
    if request.method == 'POST':
        form = BankForm(request.POST)
        if form.is_valid():
            # Save the bank details
            bank = form.save()

            # Create a new admin user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            admin_user = User.objects.create_user(username=username, password=password)

            # Associate the admin user with the bank
            bank.admin_user = admin_user
            bank.save()

            return redirect('bindex')

    return render(request, 'bank/banksignup.html', {'form': form})


from geopy.distance import geodesic

def find_closest_bank(request):
    if request.method == 'POST':
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        
        user_location = (latitude, longitude)
        bank_distances = []
        banks = Bank.objects.all()
        for bank in banks:
            bank_location = (bank.latitude, bank.longitude)
            bank_distance = geodesic(user_location, bank_location).km
            bank_distances.append((bank, bank_distance))
        bank_distances.sort(key=lambda x: x[1])
        if bank_distances:
            closest_bank = [(bank, bank_distance) for bank, bank_distance in bank_distances]
            context = {'closest_bank': closest_bank}
            return render(request, 'bank/bresult.html', context)
        else:
            message = 'No bank found.'
            context = {'message': message}
            return render(request, 'bank/bindex.html', context)
    else:
        return render(request, 'bank/bindex.html')