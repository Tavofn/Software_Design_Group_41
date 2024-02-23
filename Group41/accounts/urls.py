from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.logInPage, name='login'),
    path('', views.logInPage, name='login'),
    path('fuel_quote_history/', views.fuelQuoteHistory, name='fuel_quote_history'),
    path('fuel_quote/', views.fuelQuote, name='fuel_quote'),
    path('profile_management/', views.profileManagement),
    path('registration/', views.registrationPage, name='registration'),
]