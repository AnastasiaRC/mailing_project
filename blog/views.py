from django.views.generic import ListView, DetailView
from blog.models import Blog


class BlogListView(ListView):
    """Просмотр статей"""
    model = Blog


class BlogDetailView(DetailView):
    """Просмотр отдельной статьи"""
    model = Blog

    def get_object(self, queryset=None):
        blog = super().get_object(queryset)
        blog.views_count += 1
        blog.save()
        return blog
