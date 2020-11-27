from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from .models import Post, Comment
from .forms import CommentForm

from .services import CommentsTreeProcessing


def base(request):
    comments = Post.objects.first().comments.all()
    comments_tree = CommentsTreeProcessing.get_comments_tree(comments)
    comment_form = CommentForm()
    context = {
        'comments': comments_tree,
        'comment_form': comment_form
    }
    return render(request, 'base.html', context)


def create_comment(request):
    comment_form = CommentForm(request.POST or None)
    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.user = request.user
        new_comment.text = comment_form.cleaned_data['text']
        new_comment.content_type = ContentType.objects.get(model="post")
        new_comment.object_id = 1
        new_comment.parent = None
        new_comment.is_child = False
        new_comment.save()
    return redirect('/post-comments')


@transaction.atomic
def create_child_comment(request):
    print(request.POST.get('parentId'))
    user = User.objects.get(username=request.POST.get('user'))
    current_id = request.POST.get('id')
    text = request.POST.get('text')

    print(request.POST)

    parent_id = request.POST.get('parentId')
    parent = Comment.objects.get(id=int(current_id))

    ct_model = ContentType.objects.get(model='post')

    Comment.objects.create(
        user=user,
        text=text,
        parent=parent,
        is_child=False if not parent else True,
        content_type=ct_model,  # Post model
        object_id=1  # Record in post model
    )
    comments = Post.objects.first().comments.all()
    comments_tree = CommentsTreeProcessing.get_comments_tree(comments)
    return render(request, 'base.html', {'comments': comments_tree})

