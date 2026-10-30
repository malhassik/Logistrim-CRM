import pytest
from rest_framework.test import APIClient
from .models import Truck


@pytest.mark.django_db
def test_api_truck_list():
    Truck.objects.create(brand="Test API Brand", plate_number="API123", mileage=100)

    client = APIClient()

    response = client.get("/api/trucks/")

    assert response.status_code == 200

    assert len(response.data) == 1

    assert response.data[0]["brand"] == "Test API Brand"
