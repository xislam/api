# Generated by Django 3.1 on 2021-08-04 23:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=25, verbose_name='автор')),
                ('title', models.CharField(max_length=50, verbose_name='заголовок')),
                ('text', models.TextField(verbose_name='текст поста')),
            ],
        ),
        migrations.CreateModel(
            name='Commentary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='текст коментарии')),
                ('object_id', models.PositiveIntegerField()),
                ('timestamp', models.DateTimeField(auto_now=True, verbose_name='датасоздания коментария')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_children', to='webapp.commentary', verbose_name='родительский коментарии')),
            ],
        ),
    ]