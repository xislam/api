from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey

from pytils.translit import translify, slugify


class Post(models.Model):
    author = models.CharField(max_length=25, verbose_name="автор")
    title = models.CharField(max_length=50, verbose_name="заголовок")
    text = models.TextField(verbose_name="текст поста")

    def __str__(self):
        return self.author


class Commentary(MPTTModel):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, blank=True, null=True, )
    author = models.CharField(max_length=25)
    content = models.TextField()
    date_add = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    parent = TreeForeignKey('self', related_name='children', null=True, blank=True, db_index=True,
                            on_delete=models.CASCADE)

    class MPTTMeta:
        order_insertion_by = ['content']

    def get_full_name(self):
        names = self.get_ancestors(include_self=True).values('author')
        full_name = ' - '.join(map(lambda x: x['author'], names))
        return full_name

    def get_group_count(self):
        cats = self.get_descendants(include_self=True)
        return Group.objects.filter(categories__in=cats).count()

    def __str__(self):
        return self.content
