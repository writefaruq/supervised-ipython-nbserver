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

    def username(self):
        return self.user.username
    
    def email(self):
        return self.user.email
    
    def first_name(self):
        return self.user.first_name
    
    def last_name(self):
        return self.user.last_name
    
    def save(self, *args, **kwargs):
        if self.user.is_staff:
            self.access_enabled = True
        super(UserProfile, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Notebook Server User Setting"
    


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)



class NoteBookServerAccessConfiguration(models.Model):
    """ Manages the Notebook server access through CSV file uploads"""
    input_file = models.FileField(upload_to=nc.NB_SERVER_ACCESS_CONFIG_PATH)
    ENABLE_ACCESS, DISABLE_ACCESS = 'Enable access', 'Disable access'
    used_for = models.CharField("Used to", max_length=20, choices=((ENABLE_ACCESS, ENABLE_ACCESS), 
                                                        (DISABLE_ACCESS, DISABLE_ACCESS)), 
                                                        default=ENABLE_ACCESS)
    applied_at = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        verbose_name = "Notebook Server Access Configuration File"
        verbose_name_plural = "Notebook Server Access Configuration Files"  
    
    
    def __unicode__(self):
        return "%s" %self.input_file
    
    
    def save(self, *args, **kwargs):
        # process the input_file
        for line in self.input_file.__dict__['_file'].readlines():
            line = line.strip()
            users = User.objects.filter(username=line)
            if users:
                user = users[0]
                user_profile = user.get_profile()
                if user.is_staff or (self.used_for == self.ENABLE_ACCESS):
                    user_profile.access_enabled = True
                elif self.used_for == self.DISABLE_ACCESS:
                    user_profile.access_enabled = False
                user_profile.save()
        super(NoteBookServerAccessConfiguration, self).save(*args, **kwargs) 