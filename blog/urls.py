from django.urls import path
from django.views.decorators.cache import cache_page
from blog.views import BlogListView, BlogDetailView
from blog.apps import BlogConfig

app_name = BlogConfig.name

""" cache_page(60) - кеширование всего контроллера в течении минуты"""

urlpatterns = [
    path('list/', cache_page(60)(BlogListView.as_view()), name='blog_list'),
    path('blog_view/<int:pk>/', cache_page(60)(BlogDetailView.as_view()), name='blog_detail'),
]