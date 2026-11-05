from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Truck, Document, Driver
from .forms import DocumentForm, FuelRecordForm, DriverNotesForm
from django.db.models import Sum
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
def dashboard(request):
    trucks = Truck.objects.all()
    drivers = Driver.objects.all()

    context = {
        "trucks": trucks,
        "drivers": drivers,
    }

    return render(request, "fleet/dashboard.html", context)


@login_required
def truck_detail(request, truck_id):
    truck = get_object_or_404(Truck, id=truck_id)

    # Блок документов
    documents = truck.document_set.all()

    # Блок заправки
    fuel_records = truck.fuelrecord_set.all().order_by("-date")
    total_cost = fuel_records.aggregate(total=Sum("price"))["total"]

    if total_cost is None:
        total_cost = 0

    context = {
        "truck": truck,
        "documents": documents,
        "fuel_records": fuel_records,
        "total_cost": total_cost,
    }

    return render(request, "fleet/truck_detail.html", context)


@login_required
def driver_detail(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)

    if request.method == "POST":
        form = DriverNotesForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            return redirect("driver_detail", driver_id=driver.id)
    else:
        form = DriverNotesForm(instance=driver)

    context = {
        "driver": driver,
        "form": form,
    }

    return render(request, "fleet/driver_detail.html", context)


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
            return redirect("truck_detail", truck_id=truck_id)
    else:
        form = DocumentForm()

    return render(request, "fleet/upload_document.html", {"form": form, "truck": truck})


@login_required
@user_passes_test(is_accountant, login_url="/login/")
def add_fuel_records(request, truck_id):
    truck = get_object_or_404(Truck, id=truck_id)

    if request.method == "POST":
        form = FuelRecordForm(request.POST)

        # ВАЖНО: говорим форме, что поле truck теперь необязательное,
        # так как мы берем ID машины из URL
        form.fields["truck"].required = False

        if form.is_valid():
            # save(commit=False) позволяет создать объект в памяти, но не сохранять в БД
            record = form.save(commit=False)
            # Принудительно привязываем машину из URL
            record.truck = truck
            # Теперь сохраняем в базу
            record.save()

            # Возвращаем на страницу этой машины
            return redirect("truck_detail", truck_id=truck_id)
    else:
        form = FuelRecordForm()

    # Передаем truck в контекст, чтобы в HTML сделать красивую кнопку "Назад"
    return render(request, "fleet/fuel_form.html", {"form": form, "truck": truck})
