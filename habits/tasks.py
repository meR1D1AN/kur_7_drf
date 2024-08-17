from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from habits.services import send_telegram


@shared_task()
def habit():

    now = timezone.now()
    print(f"Текущее время: {now}")

    habits = Habit.objects.filter(
        time__lte=now, time__gt=now - timezone.timedelta(minutes=1)
    )

    print(f"Найдено привычек: {habits.count()}")

    for habit_item in habits:
        if habit_item.user.tg_chat_id:
            send_telegram(habit_item)
            if habit_item.frequency_unit == "days":
                habit_item.time = habit_item.time + timezone.timedelta(
                    days=habit_item.frequency_number
                )
            elif habit_item.frequency_unit == "hours":
                habit_item.time = habit_item.time + timezone.timedelta(
                    hours=habit_item.frequency_number
                )
            elif habit_item.frequency_unit == "minutes":
                habit_item.time = habit_item.time + timezone.timedelta(
                    minutes=habit_item.frequency_number
                )
            habit_item.save()
        else:
            print(f"У пользователя {habit_item.user} не указан тг")
