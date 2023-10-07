from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from clients.models import Client
from django.urls import reverse_lazy
from clients.forms import ClientForm
from mailing.views import AuthorAccessMixin, ManagerAuthorAccessMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Cоздание клиента"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('clients:client_list')

    def form_valid(self, form):
        """Присвоение автора"""
        if form.is_valid():
            client = form.save()
            client.author = self.request.user
            client.save()
        return super().form_valid(form)


class ClientUpdateView(AuthorAccessMixin, UpdateView):
    """Редактирование клиента"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('clients:client_list')


class ClientListView(ListView):
    """Просмотр списка клиентов"""
    model = Client

    def dispatch(self, request, *args, **kwargs):
        """Обязательная авторизация"""
        if self.request.user.is_anonymous:
            return redirect('mailing:error')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        """Каждый пользователь видит только своих клиентов, кроме менеджера он видит все контакты"""
        queryset = super().get_queryset()
        if not self.request.user.is_manager:
            queryset = queryset.filter(author=self.request.user.pk)
        return queryset


class ClientDetailView(ManagerAuthorAccessMixin, DetailView):
    """Просмотр отдельного клиента"""
    model = Client


class ClientDeleteView(AuthorAccessMixin, DeleteView):
    """Удаления клиента"""
    model = Client
    success_url = reverse_lazy('clients:client_list')
