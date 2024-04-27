from django.db import models
from django.contrib.auth.models import User
from bootstrap_datepicker_plus.widgets import DatePickerInput
# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE) # one to one relationships(one customer can have one user and one user can have one customer)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Out Door', 'Out Door'),
    )

    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag) # Many to Many relationships

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL) # one to many relationships
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL) # one to many relationships
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    note = models.CharField(max_length=1000, null=True) # for custom Search
    price = models.CharField(max_length=1000, null=True) # for custom Search
    delivery_date = models.DateField(null=True, blank=True)
    delivery_address = models.CharField(max_length=200, null=True)  # New field
    city = models.CharField(max_length=100, null=True)  # New field
    state = models.CharField(max_length=100, null=True)  # New field
    zip_code = models.CharField(max_length=20, null=True)  # New field
    gallons_requested = models.FloatField(null=True)
    has_history = models.BooleanField(null=True)
    suggested_price = models.FloatField(null=True)
    total_amount = models.FloatField(null=True)


    def __str__(self):
        return self.product.name

class FuelQuote(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL) # one to many relationships
    gallons_requested = models.FloatField()
    state = models.CharField(max_length=100)
    has_history = models.BooleanField()
    suggested_price = models.FloatField()
    total_amount = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=255, default='Unknown')  # Default value added
    city = models.CharField(max_length=100, default='Unknown')     # Default value added
    zip_code = models.CharField(max_length=20, default='00000')    # Default value added
    
    def __str__(self):
        return f"{self.address}, {self.city}, {self.state},{self.zip_code}"
    