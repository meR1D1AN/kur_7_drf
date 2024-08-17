from unittest.mock import patch

from django.test import TestCase, override_settings

from django.core.management import call_command
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from freezegun import freeze_time

from habits.models import Habit
from habits.services import send_telegram
from habits.tasks import habit
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test@gmail.com",
            tg_chat_id="12345"
        )
        self.habit = Habit.objects.create(
            place="парк",
            time=timezone.now(),
            action="приседания",
            is_pleasant=False,
            frequency_number=1,
            frequency_unit="days",
            reward="съесть яблоко",
            duration="120",
            is_public=True,
            user=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_retrieve(self):
        url = reverse("habits:habits-detail", args=(self.habit.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data.get("action"), self.habit.action)

    def test_habit_create(self):
        url = reverse("habits:habits-list")
        data = {
            "place": "дом",
            "time": timezone.now().isoformat(),
            "action": "протереть пыль",
            "is_pleasant": False,
            "frequency_number": 1,
            "frequency_unit": "days",
            "reward": "посмотреть фильм",
            "duration": "00:02:00",
            "is_public": True,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_list(self):
        url = reverse("habits:habits-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_update(self):
        url = reverse("habits:habits-detail", args=(self.habit.pk,))
        data = {
            "reward": "посмотреть фильм",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("reward"), "посмотреть фильм")

    def test_public_habit_list(self):
        url = reverse("habits:public")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_delete(self):
        url = reverse("habits:habits-detail", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)

    @patch('habits.tasks.send_telegram')
    def test_habit_task(self, mock_send_telegram):
        habit()
        updated_habit = Habit.objects.get(pk=self.habit.pk)
        self.assertGreater(updated_habit.time, self.habit.time)
        mock_send_telegram.assert_called_once_with(self.habit)


class CreateSuperUserCommandTest(TestCase):
    def test_create_superuser(self):
        call_command("csu")

        user = User.objects.get(email="a@a.ru")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password("123"))


class CreateUserCommandTest(TestCase):
    def test_create_superuser(self):
        call_command("cu")

        user = User.objects.get(email="aa@a.ru")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password("123"))


class ServiceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test@gmail.com",
            tg_chat_id="12345678"
        )

        self.habit = Habit.objects.create(
            place="парк",
            time=timezone.make_aware(timezone.datetime(2024, 8, 24, 8, 0, 0)),
            action="приседания",
            is_pleasant=False,
            frequency_number=1,
            frequency_unit="days",
            reward="съесть яблоко",
            duration="120",
            is_public=True,
            user=self.user,
        )

    @patch('requests.get')
    @override_settings(BOT_TOKEN='test_token')
    @freeze_time("2024-08-24 08:00:00")
    def test_send_telegram(self, mock_get):
        mock_get.return_value.status_code = 200
        send_telegram(self.habit)
        mock_get.assert_called_once_with(
            "https://api.telegram.org/bottest_token/sendMessage",
            params={
                "text":
                    "приседания запланировано на сегодня на 08:00",
                "chat_id":
                    "12345678"}
        )
