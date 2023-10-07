from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from django.core.management.base import BaseCommand

from mailing.models import Mailing
from users.models import User
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    def handle(self, *args, **options):
        email = input('Enter email address: ')
        password = input('Enter password: ')

        user = User.objects.create(
            email=email,
            is_manager=True,
            is_active=True
        )

        user.set_password(password)
        user.save()
        try:
            managers_group = Group.objects.get(name='Менеджер')
            self.stdout.write(self.style.SUCCESS('Группа менеджеров уже существует'))
        except Group.DoesNotExist:
            managers_group = Group.objects.create(name='Менеджер')
            self.stdout.write(self.style.SUCCESS('Группа менеджеров успешно создана'))
            user_content_type = ContentType.objects.get_for_model(User)
            mailing_content_type = ContentType.objects.get_for_model(Mailing)
            view_permission_m = Permission.objects.get(codename="view_mailing", content_type=mailing_content_type)
            view_permission_u = Permission.objects.get(codename="view_user", content_type=user_content_type)
            managers_group.permissions.add(view_permission_m, view_permission_u)
        user.groups.add(managers_group)
