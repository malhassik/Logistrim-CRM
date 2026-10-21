from django import forms
from .models import Document, FuelRecord, Truck, Driver


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["title", "truck", "file"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Например: ТН на перевозку",
                }
            ),
            "truck": forms.Select(attrs={"class": "form-control"}),
            "file": forms.FileInput(attrs={"class": "form-control"}),
        }


class FuelRecordForm(forms.ModelForm):
    class Meta:
        model = FuelRecord
        fields = ["truck", "liters", "price"]

        widgets = {
            "truck": forms.Select(attrs={"class": "form-control"}),
            "liters": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "placeholder": "Например: 150.5",
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "placeholder": "Например: 9000",
                }
            ),
        }


class TruckForm(forms.ModelForm):
    class Meta:
        model = Truck
        fields = ["brand", "plate_number", "mileage", "driver"]
        widgets = {
            "brand": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Например: Volvo"}
            ),
            "plate_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "А123ВС77"}
            ),
            "mileage": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "0"}
            ),
            "driver": forms.Select(attrs={"class": "form-control"}),
        }


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["name", "phone"]

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Например: Иван Иванов"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "+7 999 123-45-67"}
            ),
        }
