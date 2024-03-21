from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.http import HttpResponse
# Create your views here.

def logInPage(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("fuel_quote")
        else:
            print("not working")
            messages.success(request,("There was an error loggin in, try again."))
            return redirect("/")        
            
    else:
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

 
