from django.contrib import admin
from .models import Truck, Driver, Document, FuelRecord

admin.site.register(Truck)
admin.site.register(Driver)
admin.site.register(Document)
admin.site.register(FuelRecord)
