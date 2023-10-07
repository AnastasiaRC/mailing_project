from django.core.management import BaseCommand
from users.models import User
import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@shop.ru',
            first_name='Admin',
            last_name='Admin',
            is_superuser=True,
            is_staff=True,
            is_active=True
        )
        user.set_password(os.getenv('ADMIN_PASSWORD'))
        user.save()
