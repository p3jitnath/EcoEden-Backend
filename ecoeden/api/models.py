from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from datetime import datetime

from django.conf import settings

class User(AbstractUser):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile = models.CharField(validators=[phone_regex], max_length=15, unique=True) # validators should be a list
    email = models.EmailField(unique=True)
    score = models.IntegerField(default=settings.SCORE_DEFAULT)

    collections = models.IntegerField(default=0, blank=True)
    posts = models.IntegerField(default=0, blank=True)
    verifications = models.IntegerField(default=0, blank=True)

    REQUIRED_FIELDS = ['mobile', 'email']

class Photo(models.Model):

    def get_prediction(instance):
        # insert model prediction
        return True

    def file_name(instance, filename):
        now = datetime.now() 
        date_time = now.strftime("%m-%d-%Y-%H-%M-%S")
        extension = filename.split('.')[-1]
        return '{}-{}.{}'.format(instance.user.username, date_time, extension)
    
    trash = property(get_prediction)
    created_at = models.DateTimeField(auto_now_add=True)
    
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE, null=False)
    image = models.ImageField(upload_to = file_name)
    description = models.TextField(blank=True, null=True)
    lat = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=False)
    lng = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=False)
    
    upvotes = models.IntegerField(default=0, blank=True)
    downvotes = models.IntegerField(default=0, blank=True)

    visible = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user) + '-' + str(self.created_at)

class Activity(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    user = models.ForeignKey(User, related_name='activity_user', on_delete=models.CASCADE, null=False)
    photo = models.ForeignKey(Photo, related_name='activity_photo', on_delete=models.CASCADE, null=False)
    vote = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'photo')


class TrashCollection(models.Model):
    collected_at = models.DateTimeField(auto_now_add=True)
    photo = models.OneToOneField(Photo, on_delete=models.CASCADE, null=False)
    collector = models.ForeignKey(User, on_delete=models.CASCADE, related_name='poster', null=False)
    upvotes = models.IntegerField(default=0, blank=True)
    downvotes = models.IntegerField(default=0, blank=True) 
    visible = models.BooleanField(default=True)

class TrashCollectionActivity(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    user = models.ForeignKey(User, related_name='trash_collection_activity_user', on_delete=models.CASCADE, null=False)
    trash_collection = models.ForeignKey(TrashCollection, related_name='trash_collection_activity_trash_collection', on_delete=models.CASCADE, null=False)
    vote = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'trash_collection')