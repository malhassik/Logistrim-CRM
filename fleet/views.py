from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Truck, Document, FuelRecord
from .forms import DocumentForm, FuelRecordForm, TruckForm, DriverForm
from django.db.models import Sum
from django import forms
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .serializers import TruckSerializer
from rest_framework import generics, permissions


class TruckListAPIView(generics.ListCreateAPIView):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TruckDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


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
def add_fuel_records(request):
    if request.method == "POST":
        form = FuelRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse(
                {"status": "success", "message": "Заправка успешно добавлена!"}
            )
        else:
            return JsonResponse({"status": "error", "errors": form.errors}, status=400)
    else:
        form = FuelRecordForm()

    return render(request, "fleet/fuel_form.html", {"form": form})


@login_required
@user_passes_test(is_accountant, login_url="/login/")
def add_driver(request):
    if request.method == "POST":
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("truck_list")
    else:
        form = DriverForm()

    return render(request, "fleet/driver_form.html", {"form": form})


@login_required
@user_passes_test(is_accountant, login_url="/login/")
def add_truck(request):
    if request.method == "POST":
        form = TruckForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("truck_list")
    else:
        form = TruckForm()

    return render(request, "fleet/truck_form.html", {"form": form})


@login_required
@user_passes_test(is_accountant, login_url="/login/")
def edit_truck(request, truck_id):
    # 1. Находим машину в базе по её ID (если нет — выдаем ошибку 404)
    truck = get_object_or_404(Truck, id=truck_id)

    if request.method == "POST":
        # 2. Передаем существующую машину в форму (instance=truck)
        form = TruckForm(request.POST, instance=truck)
        if form.is_valid():
            form.save()  # Django обновит эту же запись, а не создаст новую
            return redirect("truck_list")
    else:
        # 3. При GET-запросе показываем форму, уже заполненную данными машины
        form = TruckForm(instance=truck)

    return render(request, "fleet/truck_form.html", {"form": form, "truck": truck})


@login_required
@user_passes_test(is_accountant, login_url="/login/")
def upload_document(request, truck_id):
    truck = get_object_or_404(Truck, id=truck_id)

    if request.method == "POST":
        form = DocumentForm(request.POST)
        files = request.FILES.getlist("files")  # Получаем список файлов

        # Проверяем: если файлы не выбраны, добавляем ошибку в форму
        if not files:
            form.add_error(None, "Выберите хотя бы один файл для загрузки.")

        if form.is_valid():
            title = form.cleaned_data["title"]
            for f in files:
                Document.objects.create(
                    title=f"{title} ({f.name})", file=f, truck=truck
                )
            return redirect("truck_list")
    else:
        form = DocumentForm()

    return render(request, "fleet/upload_document.html", {"form": form, "truck": truck})


@login_required
@user_passes_test(is_accountant, login_url="/login/")
def delete_truck(request, truck_id):
    truck = get_object_or_404(Truck, id=truck_id)
    truck.delete()
    return redirect("truck_list")


@login_required
@user_passes_test(is_accountant, login_url="/login/")
def fuel_list(request):
    records = FuelRecord.objects.all().order_by("-id")

    return render(request, "fleet/fuel_list.html", {"records": records})
