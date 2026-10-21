from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Truck, Document, FuelRecord
from .forms import DocumentForm
from django.db.models import Sum


def is_accountant(user):
    return user.is_superuser or user.groups.filter(name="Бухгалтеры").exists()


@login_required
def truck_list(request):
    trucks = Truck.objects.all()

    total_trucks = trucks.count()
    free_trucks = trucks.filter(status="Свободна").count()
    total_documents = Document.objects.count()

    fuel_expenses = FuelRecord.objects.aggregate(total=Sum("price"))["total"]
    if fuel_expenses is None:
        fuel_expenses = 0

    context = {
        "trucks": trucks,
        "total_trucks": total_trucks,
        "free_trucks": free_trucks,
        "total_documents": total_documents,
        "fuel_expenses": fuel_expenses,
    }

    return render(request, "fleet/truck_list.html", context)


@login_required
@user_passes_test(is_accountant, login_url="/login/")
def upload_document(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("truck_list")
    else:
        form = DocumentForm()

    return render(request, "fleet/upload_document.html", {"form": form})


def fuel_list(request):
    records = FuelRecord.objects.all().order_by("-id")

    return render(request, "fleet/fuel_list.html", {"records": records})
