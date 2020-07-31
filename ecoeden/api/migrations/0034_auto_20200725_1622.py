# Generated by Django 3.0.4 on 2020-07-25 16:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0033_auto_20200722_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trashcollection',
            name='collector',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='poster', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='trashcollection',
            name='photo',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.Photo'),
            preserve_default=False,
        ),
    ]
