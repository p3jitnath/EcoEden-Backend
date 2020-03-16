from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from datetime import datetime

class User(AbstractUser):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile = models.CharField(validators=[phone_regex], max_length=17) # validators should be a list
    score = models.IntegerField(default=0)
    REQUIRED_FIELDS = ['mobile']

class TrashCollection(models.Model):

    def get_time_of_verification(instance):
        if instance.verified is not None:
            return datetime.now()
        else:
            return None

    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploader')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    collector = models.ForeignKey(User, on_delete=models.CASCADE, related_name='poster', null=True)
    verified = models.NullBooleanField(null=True)
    verified_at = property(get_time_of_verification)

class Photo(models.Model):

    def get_prediction(instance):
        # insert model prediction
        return False

    def file_name(instance, filename):
        now = datetime.now()
        date_time = now.strftime("%m-%d-%Y-%H-%M-%S")
        extension = filename.split('.')[-1]
        return '{}-{}.{}'.format(instance.user.username, date_time, extension)
    
    trash = property(get_prediction)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to = file_name)
    description = models.TextField(blank=True, null=True)
    lat = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    lng = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)