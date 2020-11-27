from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation


class Post(models.Model):

    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='related_post',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    comments = GenericRelation('comment')

    def __str__(self):
        return str(self.id)


class Comment(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='related_comment',
                               on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey('self',
                               verbose_name='parent comment',
                               null=True,
                               blank=True,
                               related_name='child_comment',
                               on_delete=models.CASCADE)
    is_child = models.BooleanField(default=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    createdAt = models.DateTimeField(auto_now=True, verbose_name='Created at')

    @property
    def get_parent(self):
        if not self.parent:
            return ''
        return self.parent

    def __str__(self):
        return str(self.id)

