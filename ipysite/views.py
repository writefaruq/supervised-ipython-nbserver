import os
import subprocess
import time
import string
import random
import csv

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse

from IPython.lib import passwd

from ipysite.models import UserProfile 
import ipysite.notebook_config as nc

from utils import common_settings as cs


def homepage(request):
    """ Shows homepage """
    return render_to_response('homepage.html', {}, context_instance=RequestContext(request))


def _get_nbserver_settings(user_id, config_file):
    #read setings from a shared settings file
    port, password = None, 'Unset'
    config = open(config_file, 'r')
    reader = csv.reader(config)
    for row in reader:
        server_id = row[cs.NBSERVER_ALL_CONFIG_ID_COLUMN]
        if int(user_id) == int(server_id):
            port = row[cs.NBSERVER_ALL_CONFIG_PORT_COLUMN]
            password =  row[cs.NBSERVER_ALL_CONFIG_PASSWORD_COLUMN]
            break
    if port is None:
        raise Exception("Failed to find a matching port number for user_id: %s in config file: %s" %(user_id, config_file))
    return (port, password)
    



def account_settings(request):
    """ Shows the Notebook server settings """
    username = request.user.username

    u = User.objects.get(username=username)
    users =  UserProfile.objects.filter(user=u)
    if users:
        user_profile = users[0]
    else:
        user_profile = UserProfile.objects.create(user=u)
    
    # check the port setup
    user_id = user_profile.user.id
    config_file =  nc.NB_SERVER_SETTINGS_FILE
    nbserver_settings = _get_nbserver_settings(user_id, config_file)
    #print "USER:%s --> settings: %s" %(user_id, nbserver_settings)
    if nbserver_settings:
        user_profile.nbserver_port = nbserver_settings[0]
        user_profile.nbserver_password =  nbserver_settings[1]
        user_profile.save()
    # show the settings
    if user_profile.user.is_staff or user_profile.access_enabled:
        ctx =  {'nbserver_password' : user_profile.nbserver_password,
            'nbserver_url' : '{0}:{1}'.format(nc.BASE_URL, user_profile.nbserver_port)}
        return render_to_response('account/settings.html', ctx, context_instance=RequestContext(request))
    else:
        return render_to_response('error_message.html', {}, context_instance=RequestContext(request))




