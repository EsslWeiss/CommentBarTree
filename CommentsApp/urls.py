from django.urls import path
from .views import base, create_comment, create_child_comment


urlpatterns = [
    path('post-comments/', base, name='post-comments'),
    path('create-comment/', create_comment, name='create-comment'),
    path('create-child-comment/', create_child_comment, name='create-child-comment'),
]

