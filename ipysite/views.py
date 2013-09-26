import os
import subprocess
import time
import string
import random
import csv
import socket
from urlparse import urlparse

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
    

def is_port_open(host, port):
    """ Scan the Notebook server post"""
    #Create socket
    try:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except socket.error, err_msg:
        return False
     
    #Get IP of remote host
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.error,error_msg:
        return False
     
    #Scan port
    try:
        sock.connect((remote_ip,port))
        sock.close()
        return True
    except socket.error:
        pass # skip various socket error



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
    if nbserver_settings:
        user_profile.nbserver_port = nbserver_settings[0]
        user_profile.nbserver_password =  nbserver_settings[1]
        user_profile.save()
    # test the port if open
    url = urlparse(nc.BASE_URL)
    port_open = is_port_open(url.netloc, int(user_profile.nbserver_port))
    
    # show the settings
    if user_profile.user.is_staff or user_profile.access_enabled:
        if not port_open:
            return render_to_response('error_message.html', 
                {'msg_title' : "Sorry, your Notebook server is not running yet.",
                'error_details' : "Notebook server is not running on port %s. Please contact your course administrator for help." %user_profile.nbserver_port},
                context_instance=RequestContext(request))
        ctx =  {'nbserver_password' : user_profile.nbserver_password,
        'nbserver_url' : '{0}:{1}'.format(nc.BASE_URL, user_profile.nbserver_port)}
        return render_to_response('account/settings.html', ctx, context_instance=RequestContext(request))
    else:
        return render_to_response('error_message.html', 
                                  {'msg_title' : "Unauthorized access is not allowed.",
                                   'error_details' : "You are not authorized yet to access the Notebook server. Please contact your course administrator for help."},
                                  context_instance=RequestContext(request))




