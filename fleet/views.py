from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Truck, Document, Driver, TripLog
from .forms import (
    DocumentForm,
    FuelRecordForm,
    DriverNotesForm,
    DriverAvatarForm,
    TripLogForm,
)
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
    trucks = Truck.objects.select_related("driver")
    drivers = Driver.objects.all()

    context = {
        "trucks": trucks,
        "drivers": drivers,
    }

    return render(request, "fleet/dashboard.html", context)


@login_required
def trip_log(request):

    if request.method == "POST":
        form = TripLogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("trip_log")
    else:
        form = TripLogForm()

    logs = TripLog.objects.all().order_by("-date")

    context = {
        "form": form,
        "logs": logs,
    }

    return render(request, "fleet/trip_log.html", context)


@login_required
def truck_detail(request, truck_id):
    truck = get_object_or_404(Truck, id=truck_id)

    context = {
        "truck": truck,
    }

    return render(request, "fleet/truck_detail.html", context)


@login_required
def driver_detail(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)

    # 1. Создаем обе формы заранее (с текущими данными водителя для GET)
    avatar_form = DriverAvatarForm(instance=driver)
    notes_form = DriverNotesForm(instance=driver)

    # 2. Если пришел POST-запрос, обновляем нужную форму
    if request.method == "POST":
        if "avatar" in request.FILES:
            avatar_form = DriverAvatarForm(request.POST, request.FILES, instance=driver)
            if avatar_form.is_valid():
                avatar_form.save()
                return redirect("driver_detail", driver_id=driver.id)

        # Иначе, если нажата кнопка сохранения заметок
        elif "submit_notes" in request.POST:
            notes_form = DriverNotesForm(request.POST, instance=driver)
            if notes_form.is_valid():
                notes_form.save()
                return redirect("driver_detail", driver_id=driver.id)

    # 3. Передаем обе формы в шаблон (они всегда существуют)
    context = {
        "driver": driver,
        "notes_form": notes_form,
        "avatar_form": avatar_form,
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
