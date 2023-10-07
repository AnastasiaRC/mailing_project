from django.urls import path
from clients.apps import ClientsConfig
from clients.views import ClientListView, ClientCreateView, ClientUpdateView, ClientDetailView, ClientDeleteView

app_name = ClientsConfig.name

urlpatterns = [
    path('list/', ClientListView.as_view(), name='client_list'),
    path('create/', ClientCreateView.as_view(), name='client_create'),
    path('edit/<int:pk>/', ClientUpdateView.as_view(), name='client_edit'),
    path('view/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
]
