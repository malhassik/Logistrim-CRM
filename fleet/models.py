from django.db import models


class Driver(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя водителя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")

    def __str__(self):
        return self.name


class Truck(models.Model):
    plate_number = models.CharField(max_length=20, verbose_name="Госномер")
    brand = models.CharField(max_length=50, verbose_name="Марка")
    mileage = models.IntegerField(default=0, verbose_name="Пробег (км)")
    status = models.CharField(max_length=50, default="Свободна", verbose_name="Статус")

    driver = models.ForeignKey(
        Driver,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Водитель",
    )

    def __str__(self):
        if self.driver is not None:
            return f"{self.brand} — {self.plate_number} | Водитель: {self.driver.name}"
        return f"{self.brand} — {self.plate_number} | Водитель: не назначен"

    def save(self, *args, **kwargs):
        if self.driver is not None:
            self.status = "Занята"
        else:
            self.status = "Свободна"

        super().save(*args, **kwargs)


class FuelRecord(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, verbose_name="Машина")
    liters = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name="Количество литров"
    )
    price = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Стоимость (руб)"
    )
    date = models.DateField(auto_now_add=True, verbose_name="Дата заправки")

    def __str__(self):
        return f"{self.truck.plate_number} - {self.liters} л."


class Document(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название (НТ, Чек)")
    file = models.FileField(upload_to="documents/", verbose_name="Файл")
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, verbose_name="Машина")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")

    def __str__(self):
        return f"{self.title} - {self.truck.plate_number}"
