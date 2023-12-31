from django.contrib import admin
from mailing.models import Mailing


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('message', 'time_start', 'time_end', 'period', 'status',)
