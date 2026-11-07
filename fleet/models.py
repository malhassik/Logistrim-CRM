from django.db import models
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator
from django.db.models import Sum
from django.shortcuts import redirect


class Driver(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Имя водителя",
    )
    phone = PhoneNumberField(
        verbose_name="Телефон",
        unique=True,
    )
    notes = models.TextField(
        blank=True,
        verbose_name="Заметки",
    )
    license_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="ВУ",
        validators=[
            RegexValidator(
                regex=r"^\d{10}$",  # Регулярное выражение: ровно 10 цифр
                message="Номер ВУ должен состоять ровно из 10 цифр",
            )
        ],
        null=True,
        blank=True,
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        null=True,
        blank=True,
        verbose_name="Аватарка",
    )

    @property
    def formatted_license(self):
        if not self.license_number:
            return "Не указан"
        num = str(self.license_number)

        return f"{num[:2]} {num[2:4]} {num[4:]}"

    def __str__(self):
        return self.name


class Truck(models.Model):
    plate_number = models.CharField(
        max_length=20,
        verbose_name="Госномер",
        unique=True,
    )
    brand = models.CharField(
        max_length=50,
        verbose_name="Марка",
    )
    mileage = models.IntegerField(
        default=0,
        verbose_name="Пробег (км)",
        validators=[MinValueValidator(0)],
    )
    status = models.CharField(
        max_length=50,
        default="Свободна",
        verbose_name="Статус",
    )
    driver = models.ForeignKey(
        Driver,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Водитель",
    )

    def save(self, *args, **kwargs):
        if self.driver is not None:
            self.status = "Занята"
        else:
            self.status = "Свободна"

        self.plate_number = self.plate_number.upper()

        super().save(*args, **kwargs)

    @property
    def documents(self):
        return self.document_set.all()

    @property
    def fuel_records(self):
        return self.fuelrecord_set.all().order_by("-date")

    @property
    def total_fuel_cost(self):
        return self.fuelrecord_set.aggregate(total=Sum("price"))["total"] or 0

    def __str__(self):
        if self.driver is not None:
            return f"{self.brand} — {self.plate_number} | Водитель: {self.driver.name}"
        return f"{self.brand} — {self.plate_number} | Водитель: не наёначен"


class FuelRecord(models.Model):
    truck = models.ForeignKey(
        Truck,
        on_delete=models.CASCADE,
        verbose_name="Машина",
    )
    liters = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Количество литров",
        validators=[MinValueValidator(0.01)],
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Стоимость (руб)",
        validators=[MinValueValidator(0.01)],
    )
    date = models.DateField(
        auto_now_add=True,
        verbose_name="Дата заправки",
    )

    def __str__(self):
        return f"{self.truck.plate_number} - {self.liters} л."


class Document(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название (НТ, Чек)",
    )
    file = models.FileField(
        upload_to="documents/",
        verbose_name="Файл",
    )
    truck = models.ForeignKey(
        Truck,
        on_delete=models.CASCADE,
        verbose_name="Машина",
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата загрузки",
    )

    def __str__(self):
        return f"{self.title} - {self.truck.plate_number}"


class TripLog(models.Model):
    date = models.DateField(
        verbose_name="Дата рейса",
    )
    route = models.CharField(
        max_length=50,
        verbose_name="Маршрут",
    )
    distance = models.IntegerField(
        verbose_name="Расстояние",
        validators=[MinValueValidator(0)],
    )
    mileage = models.IntegerField(
        verbose_name="Пробег (км)",
        validators=[MinValueValidator(0)],
    )
    loading_weight_kg = models.IntegerField(
        verbose_name="Вес загрузки",
        validators=[MinValueValidator(0)],
    )
    unloading_weight_kg = models.IntegerField(
        verbose_name="Вес выгрузки",
        validators=[MinValueValidator(0)],
    )
