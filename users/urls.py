from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, ActivateView, UserListView, UserUpdateView, \
    RegistrEmailView, VerificationView

app_name = UsersConfig.name


urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register_need_verify', RegistrEmailView.as_view(), name='register_need_verify'),
    path('verification_success/', VerificationView.as_view(), name='verification_success'),
    path('activate/<uidb64>/<token>', ActivateView.as_view(), name='activate'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('list/', UserListView.as_view(), name='user_list'),
    path('edit/<int:pk>/', UserUpdateView.as_view(), name='user_edit'),
]
