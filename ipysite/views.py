import os
import subprocess
import time
import string
import random

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse

from IPython.lib import passwd

from ipysite.models import UserProfile 
import ipysite.notebook_config as nc


def homepage(request):
    """ Shows homepage """
    return render_to_response('homepage.html', 
                              {},
                               context_instance=RequestContext(request))


def account_settings(request):
    """ Shows the Notebook server settings """
    username = request.user.username

    u = User.objects.get(username=username)
    users =  UserProfile.objects.filter(user=u)
    if users:
        user_profile = users[0]
    else:
        user_profile = UserProfile.objects.create(user=u)
        user_profile.nbserver_port = '101'
        user_profile.nbserver_password =  'ABCD'
        user_profile.save()
    # show the settings
    if user_profile.user.is_staff or user_profile.access_enabled:
        ctx =  {'nbserver_password' : user_profile.nbserver_password,
            'nbserver_url' : '{0}:{1}'.format(nc.BASE_URL, user_profile.nbserver_port)}
        return render_to_response('account/settings.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponse("<html> Unauthorized access to the Notebook server is disabled . Please contact your course administrator for help.</html>")




