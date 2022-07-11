from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import timedelta

# Create your models here.
class Ride(models.Model):
    route = models.CharField(max_length=100)
    date = models.DateField('ride date')
    distance = models.FloatField()
    elevation = models.IntegerField()
    duration = models.DurationField(
        default = timedelta(
            hours=0,
            minutes=0,
            seconds=0,
        )
    )
    avg_speed = models.FloatField(verbose_name=('Average Speed'))
    description = models.TextField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    