from django.urls import re_path
from .views import BlogPostRUDView


urlpatterns = [
    re_path('(?P<pk>\d+)', BlogPostRUDView.as_view(), name='post-rud')
]
