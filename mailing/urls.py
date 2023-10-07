from django.urls import path
from mailing.views import HomeView, MailingListView, MailingCreateView, MailingDetailView, AccessErrorView, MailingUpdateView, MailingDeleteView, LogListView, LogDetailView
from mailing.apps import MailingConfig

app_name = MailingConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('error/', AccessErrorView.as_view(), name='error'),
    path('create/', MailingCreateView.as_view(), name='mailing_create'),
    path('list/', MailingListView.as_view(), name='mailing_list'),
    path('edit/<int:pk>/', MailingUpdateView.as_view(), name='mailing_edit'),
    path('view/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('log_view/<int:pk>/', LogDetailView.as_view(), name='log_detail'),
    path('log_list/', LogListView.as_view(), name='log_list'),
]
