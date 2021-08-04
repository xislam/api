from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Post(models.Model):
    author = models.CharField(max_length=25, verbose_name="автор")
    title = models.CharField(max_length=50, verbose_name="заголовок")
    text = models.TextField(verbose_name="текст поста")
    comments = GenericRelation('commentary')

    def __str__(self):
        return self.author


class Commentary(models.Model):
    text = models.TextField(verbose_name="текст коментарии")
    parent = models.ForeignKey('self', verbose_name="родительский коментарии", blank=True, null=True,
                               on_delete=models.CASCADE, related_name="comment_children")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now=True, verbose_name="датасоздания коментария")

    def __str__(self):
        return str(self.id)
