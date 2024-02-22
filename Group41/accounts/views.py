from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def logInPage(request):
    return render (request, 'accounts/login.html')
def fuelQuoteHistory(request):
    return render (request, 'accounts/fuel_quote_history.html')
def fuelQuote(request):
    return render (request, 'accounts/fuel_quote.html')
def profileManagement(request):
    return render (request, 'accounts/profile_management.html')
def registrationPage(request):
    return render (request, 'accounts/registration.html')
def signUp(request):
    return render (request, 'accounts/signup.html')

 
