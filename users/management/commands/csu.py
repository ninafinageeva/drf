from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email="finageeva.nina@mail.ru",
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )

        user.set_password("54321")
        user.save()
