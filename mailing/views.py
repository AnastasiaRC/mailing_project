import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from clients.models import Client
from mailing.models import Mailing, Log
from django.urls import reverse_lazy
from mailing.forms import MailingForm, MailingManagerForm
from mailing.services import get_cashed_blog_list


class ManagerAccessMixin(DetailView):
    """Права доступа только менеджеру либо ошибка"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_manager:
            return redirect('mailing:error')
        return super().dispatch(request, *args, **kwargs)


class AuthorAccessMixin(DetailView):
    """Права доступа только атору либо ошибка"""

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            return redirect('mailing:error')
        return super().dispatch(request, *args, **kwargs)


class ManagerAuthorAccessMixin(DetailView):
    """Права доступа атору и менеджеру либо ошибка"""

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not request.user.is_manager and obj.author != request.user:
            return redirect('mailing:error')
        return super().dispatch(request, *args, **kwargs)


class HomeView(TemplateView):
    """Просмотр домашней страницы"""
    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        """Вывод 3 рандомных статей, подсчет количество рассылок, активных рассылок, уникальных клиентов"""
        context_data = super().get_context_data(**kwargs)
        blog_list = list(get_cashed_blog_list())
        if len(blog_list) >= 3:
            blog_random_list = random.sample(blog_list, 3)
            context_data['blog_list'] = blog_random_list
        context_data['mailing_count'] = Mailing.objects.all().count()
        context_data['mailing_started_count'] = Mailing.objects.filter(status='started').count()
        context_data['mailing_clients_count'] = Client.objects.all().count()
        return context_data


class MailingCreateView(LoginRequiredMixin, CreateView):
    """Cоздания рассылки"""
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class=None)
        form.fields['contacts'].queryset = form.fields['contacts'].queryset.filter(author=self.request.user.id)
        return form

    def form_valid(self, form):
        """Присвоение атора при создании рассылки"""
        if form.is_valid():
            mailing = form.save()
            mailing.author = self.request.user
            mailing.save()
        return super().form_valid(form)


class MailingListView(ListView):
    """Просмотр списка рассылок"""
    model = Mailing
    ordering = ['-id']

    def get_queryset(self, *args, **kwargs):
        """Каждый пользователь видит только свои рассылки, кроме менеджера он видит все рассылки"""
        queryset = super().get_queryset()
        if not self.request.user.is_manager:
            queryset = queryset.filter(author=self.request.user.pk)
        return queryset


class MailingUpdateView(ManagerAuthorAccessMixin, UpdateView):
    """Редактирование рассылки"""
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form(self, form_class=None):
        """Менеджер может изменить только статус рассылки"""
        if form_class is None:
            form_class = self.get_form_class()
        if self.request.user.is_manager:
            return MailingManagerForm(**self.get_form_kwargs())
        return super().get_form(form_class)


class MailingDetailView(ManagerAuthorAccessMixin, DetailView):
    """Просмотр одной рассылки"""
    model = Mailing


class MailingDeleteView(AuthorAccessMixin, DeleteView):
    """Удаления рассылки"""
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')


class AccessErrorView(TemplateView):
    """Oшибки доступа"""
    template_name = 'mailing/error.html'


class LogListView(ListView):
    """Просмотр логов"""
    model = Log

    def dispatch(self, request, *args, **kwargs):
        """Обязательная авторизация либо ошибка доступа"""
        if self.request.user.is_anonymous:
            return redirect('mailing:error')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        """Каждый пользователь видит только свои логи рассылок кроме менеджера"""
        context_data = super().get_context_data(**kwargs)
        object_list_ = []
        for log in Log.objects.all():
            if log.mailing.author == self.request.user or self.request.user.is_manager:
                object_list_.append(log)
        object_list_.reverse()
        context_data['object_list'] = object_list_
        return context_data


class LogDetailView(DetailView):
    """Просмотр отдельного лога"""
    model = Log

    def dispatch(self, request, *args, **kwargs):
        """Каждый пользователь может переходить только по своему логу рассылок кроме менеджера"""
        object_ = self.get_object()
        if (object_.mailing.author != request.user) and (not self.request.user.is_manager):
            return redirect('mailing:error')
        return super().dispatch(request, *args, **kwargs)



