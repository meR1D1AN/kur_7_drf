from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(email="aa@a.ru")
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        user.set_password("123")
        user.save()
