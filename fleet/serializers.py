from rest_framework import serializers
from .models import Truck


class TruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = ["id", "brand", "plate_number", "mileage", "status", "driver"]
