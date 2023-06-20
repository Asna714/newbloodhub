from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class Donor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/Donor/',null=True,blank=True)
    bloodgroup=models.CharField(max_length=10)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    last_donation_date = models.DateField(null=True, blank=True)
   
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    
    @property
    def get_instance(self):
        return self
    
    @property
    def can_donate(self):
        if not self.last_donation_date:
            return True
        days_since_last_donation = (datetime.today().date() - self.last_donation_date).days
        return days_since_last_donation >= 56
    
    def __str__(self):
        return self.user.first_name

class BloodDonate(models.Model): 
    donor=models.ForeignKey(Donor,on_delete=models.CASCADE)   
    disease=models.CharField(max_length=100,default="Nothing")
    age=models.PositiveIntegerField()
    bloodgroup=models.CharField(max_length=10)
    unit=models.PositiveIntegerField(default=0)
    status=models.CharField(max_length=20,default="Pending")
    date=models.DateField(auto_now=True)
    
    def __str__(self):
        return self.donor
