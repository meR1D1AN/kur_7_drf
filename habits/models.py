from django.conf import settings
from django.db import models

NULLABLE = {"null": True, "blank": True}


class Habit(models.Model):
    FREQUENCY_UNITS = [
        ("minutes", "минуты"),
        ("hours", "часы"),
        ("days", "дни"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец привычки",
        **NULLABLE,
    )
    place = models.CharField(
        max_length=200,
        verbose_name="Место привычки",
    )
    time = models.DateTimeField(
        verbose_name="Дата и время привычки",
    )
    action = models.CharField(
        max_length=200,
        verbose_name="Действие",
    )
    is_pleasant = models.BooleanField(
        verbose_name="Приятная",
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        verbose_name="Родственная привычка",
        **NULLABLE,
    )
    frequency_number = models.PositiveIntegerField(
        verbose_name="Количество раз"
    )
    frequency_unit = models.CharField(
        max_length=10,
        choices=FREQUENCY_UNITS,
        default="days",
        verbose_name="Единицы измерения",
    )
    reward = models.CharField(
        max_length=200,
        verbose_name="Вознаграждение",
        **NULLABLE,
    )
    duration = models.DurationField(
        verbose_name="Длительность действия"
    )
    is_public = models.BooleanField(
        default=True,
        verbose_name="Публичная"
    )

    def __str__(self):
        return f"{self.user} - {self.action}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
