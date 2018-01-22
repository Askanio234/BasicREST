from django.urls import re_path, path
from .views import BlogPostRUDView, BlogPostCreateView


urlpatterns = [
    re_path('(?P<pk>\d+)', BlogPostRUDView.as_view(), name='post-rud'),
    path('', BlogPostCreateView.as_view(), name='post-create'),
]
