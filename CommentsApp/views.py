from django.shortcuts import render
from .models import Post, Comment


def base(request):
    comments = Post.objects.first().comments.all()
    return render(request, 'base.html', {'comments': comments})

