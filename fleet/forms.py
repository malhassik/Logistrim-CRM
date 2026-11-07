from django import forms
from .models import Document, FuelRecord, Driver, TripLog


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["title"]  # Оставляем только название, файлы обработаем во view
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Например: ТН на перевозку",
                }
            ),
        }


class FuelRecordForm(forms.ModelForm):
    class Meta:
        model = FuelRecord
        fields = [
            "truck",
            "liters",
            "price",
        ]

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


class DriverNotesForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["notes"]
        widgets = {
            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Напишите что-нибудь о водителе...",
                    "style": "width: 100%; background: #2d2d2d; color: white; border: 1px solid #444; border-radius: 5px; padding: 10px; box-sizing: border-box; font-family: inherit;",
                }
            ),
        }


class DriverAvatarForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["avatar"]


class TripLogForm(forms.ModelForm):
    class Meta:
        model = TripLog
        fields = [
            "date",
            "route",
            "distance",
            "mileage",
            "loading_weight_kg",
            "unloading_weight_kg",
        ]
