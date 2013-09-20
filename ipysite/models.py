import os

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


import notebook_config as nc

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)
    
    # Other fields here
    nbserver_port = models.IntegerField("Notebook server port", unique=True, default=0)
    nbserver_password = models.CharField("Notebook server password", max_length=16, null=True)
    access_enabled = models.BooleanField("Can access Notebook server", default=False)



def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)


