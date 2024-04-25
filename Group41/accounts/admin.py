from django.contrib import admin
from .models import *

class FuelQuoteAdmin(admin.ModelAdmin):
    list_display = ['address', 'city', 'state', 'zip_code', 'gallons_requested', 'has_history', 'suggested_price', 'total_amount', 'date_created']
    list_filter = ['state', 'has_history']
    search_fields = ['address', 'city', 'zip_code']


admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Order)
admin.site.register(FuelQuote, FuelQuoteAdmin)
