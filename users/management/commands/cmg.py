from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from django.core.management.base import BaseCommand
from users.models import User
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    def handle(self, *args, **options):
        email = input('Enter email address: ')
        password = input('Enter password: ')

        user = User.objects.create(
            email=email,
            is_staff=True,
            is_active=True
        )

        user.set_password(password)
        user.save()
        try:
            managers_group = Group.objects.get(name='Блог Менеджер')
            self.stdout.write(self.style.SUCCESS('Группа менеджеров уже существует'))
        except Group.DoesNotExist:
            managers_group = Group.objects.create(name='Блог Менеджер')
            self.stdout.write(self.style.SUCCESS('Группа менеджеров успешно создана'))
            blog_content_type = ContentType.objects.get_for_model(Blog)
            add_permission = Permission.objects.get(codename="add_blog", content_type=blog_content_type)
            change_permission = Permission.objects.get(codename="change_blog", content_type=blog_content_type)
            delete_permission = Permission.objects.get(codename="delete_blog", content_type=blog_content_type)
            managers_group.permissions.add(add_permission, change_permission, delete_permission)
        user.groups.add(managers_group)
