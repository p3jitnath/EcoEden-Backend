# Generated by Django 3.0.4 on 2020-03-15 20:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20200315_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trashcollection',
            name='collector',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='poster', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='trashcollection',
            name='uploader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploader', to=settings.AUTH_USER_MODEL),
        ),
    ]