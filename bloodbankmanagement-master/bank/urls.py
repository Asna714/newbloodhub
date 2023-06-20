from django.urls import path

from django.contrib.auth.views import LoginView
from . import views
urlpatterns = [
    path('bindex', views.find_closest_bank,name='bindex'),
    path('banksignup', views.bank_signup_view,name='banksignup'),
    path('bresult', LoginView.as_view(template_name='bank/bresult.html'),name='bresult'),
]
    