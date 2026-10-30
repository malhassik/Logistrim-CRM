import pytest
from .models import Truck, Driver


@pytest.mark.django_db
def test_truck_status_change_with_driver():
    driver = Driver.objects.create(name="Тестовый водитель", phone="+79999999999")

    truck = Truck.objects.create(brand="TestBrand", plate_number="Т001ТТ", mileage=0)

    assert truck.status == "Свободна"

    truck.driver = driver
    truck.save()

    assert truck.status == "Занята"
