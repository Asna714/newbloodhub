from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Bank

from django.contrib.auth.models import User



class BankForm(UserCreationForm, forms.ModelForm):
    name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    latitude = forms.DecimalField(max_digits=9, decimal_places=6, required=False)
    longitude = forms.DecimalField(max_digits=9, decimal_places=6, required=False)
    mobile = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Bank
        fields = ('name', 'address', 'latitude', 'longitude', 'mobile')

    def save(self, commit=True):
        bank = super().save(commit=False)
        if commit:
            bank.save()

            username = self.cleaned_data['username']
            password = self.cleaned_data['password1']

            user = User.objects.create_user(username=username, password=password)
            user.is_staff = True  # Grant admin privileges
            user.save()

            bank.admin_user = user
            bank.save()

        return bank

