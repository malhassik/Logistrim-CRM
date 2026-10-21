from django import forms
from .models import Document, FuelRecord


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
