from django.contrib.auth.mixins import LoginRequiredMixin
from mailing.views import AuthorAccessMixin, ManagerAuthorAccessMixin
from message.forms import MessageForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from message.models import Message
from django.shortcuts import redirect


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Cоздания сообщения для рассылки"""
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message:message_list')

    def form_valid(self, form):
        """Присвоение автора"""
        if form.is_valid():
            message = form.save()
            message.author = self.request.user
            message.save()
        return super().form_valid(form)


class MessageListView(ListView):
    """Просмотр списка сообщений"""
    model = Message

    def dispatch(self, request, *args, **kwargs):
        """Обязательная авторизация"""
        if self.request.user.is_anonymous:
            return redirect('mailing:error')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        """Каждый пользователь видит только свои смс, кроме менеджера он видит все контакты"""
        queryset = super().get_queryset()
        if not self.request.user.is_manager:
            queryset = queryset.filter(author=self.request.user.pk)
        return queryset


class MessageDetailView(ManagerAuthorAccessMixin, DetailView):
    """Просмотр отдельного сообщения"""
    model = Message


class MessageUpdateView(AuthorAccessMixin, UpdateView):
    """Редактирования сообщения"""
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message:message_list')


class MessageDeleteView(AuthorAccessMixin, DeleteView):
    """Удаления сообщения"""
    model = Message
    success_url = reverse_lazy('message:message_list')
