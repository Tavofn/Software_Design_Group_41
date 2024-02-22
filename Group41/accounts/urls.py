from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.logInPage, name='login'),
    path('fuel_quote_history/', views.fuelQuoteHistory),
    path('fuel_quote/', views.fuelQuote),
    path('profile_management/', views.profileManagement),
    path('registration/', views.registrationPage),
    path('signup/', views.signUp, name='signup'),

]