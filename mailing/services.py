from django.core.mail import send_mail
from django.core.cache import cache
import datetime
from mailing.models import Mailing, Log
from django.conf import settings
from blog.models import Blog
from django.utils import timezone


def get_cashed_blog_list():
    """Закешированный список статей"""
    key = 'blog'
    blog_list = Blog.objects.all()
    if settings.CACHE_ENABLED:
        blogs = cache.get(key)
        if blogs is None:
            blogs = blog_list
            cache.set(key, blogs)
        return blogs
    return blog_list


def send_email(mailing, client):
    """ Отправки сообщения """
    clients_list = [client.email]
    try:
        send_mail(
            subject=mailing.message.topic,
            message=mailing.message.text,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=clients_list,
            fail_silently=False
        )
        try_status = 'OK'
        server_answer = 'Письмо успешно отправлено'
    except Exception as error:
        try_status = 'Ошибка'
        server_answer = error
    else:
        try_status = 'ОК'
    last_try_date = timezone.now()
    Log.objects.create(mailing=mailing, contacts=client, try_status=try_status,
                       server_answer=server_answer, last_try_date=last_try_date)


def send_mails():
    """Запуск рассылки"""
    now = timezone.now()
    for mailing in Mailing.objects.filter(status='create'):
        if now >= mailing.time_start:
            mailing.status = 'started'
            mailing.save()
    for mailing in Mailing.objects.filter(status='started'):
        for contact in mailing.contacts.all():
            log = Log.objects.filter(mailing=mailing, contacts=contact)
            """ При повторной отправке """
            if log.exists():
                try_date = log.order_by('-last_try_date').first().last_try_date
                if now < mailing.time_end:
                    if mailing.period == 'daily':  # раз в день
                        if (now - try_date).days >= 1:
                            send_email(mailing, contact)
                    elif mailing.period == 'weekly':  # раз в неделю
                        if (now - try_date).days >= 7:
                            send_email(mailing, contact)
                    elif mailing.period == 'monthly':  # раз в месяц
                        if (now - try_date).days >= 30:
                            send_email(mailing, contact)
                else:
                    mailing.status = 'ended'
                    mailing.save()
            else:
                if now >= mailing.time_start:
                    send_email(mailing, contact)
