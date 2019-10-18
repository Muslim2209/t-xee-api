from django.contrib import admin

from .models import TaxiUser, Driver, Passenger, Order

admin.site.register(TaxiUser)
admin.site.register(Driver)
admin.site.register(Passenger)
admin.site.register(Order)
