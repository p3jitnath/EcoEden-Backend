# Generated by Django 3.0.4 on 2020-07-12 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_auto_20200712_0900'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trashcollection',
            name='downvotes',
        ),
        migrations.RemoveField(
            model_name='trashcollection',
            name='upvotes',
        ),
        migrations.AddField(
            model_name='photo',
            name='downvotes',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='upvotes',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
