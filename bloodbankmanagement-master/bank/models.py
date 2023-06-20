from django.db import models
from django.contrib.auth.models import User

class Bank(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def get_instance(self):
        return self
