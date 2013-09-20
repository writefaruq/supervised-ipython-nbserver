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
from ipysite import user_login


def homepage(request):
    """ Shows homepage """
    return render_to_response('homepage.html', 
                              {},
                               context_instance=RequestContext(request))


def account_settings(request):
    """ Shows the Notebook server settings """
    username = request.user.username
   
    # first time actions
    user_login.initialize_user_path(username)


    u = User.objects.get(username=username)
    users =  UserProfile.objects.filter(user=u)
    if users:
        user = users[0]
    else:
	user = UserProfile.objects.create(user=u)
        user.nbserver_port = nc.NB_SERVER_PORT_BASE + int(user.user.id)
        user.nbserver_password = _get_nbserver_password()
        user.save()

    # Run the server, if not running yet
    if os.path.exists('/proc/{0}'.format(user.nbserver_pid)): # nb server already up
        time.sleep(1)
    else: # first time or server not running
        ip_dir = '{0}/{1}/.ipython'.format(nc.DATA_DIR, username)
        nbserver_password_sha1 = passwd(user.nbserver_password)
        user.nbserver_pid = _run_server(ip_dir, user.nbserver_port, nbserver_password_sha1)
        user.save()
        # sleep to let server start listening
        time.sleep(3)

    ctx =  {'nbserver_password' : user.nbserver_password,
            'nbserver_url' : '{0}:{1}'.format(nc.BASE_URL, user.nbserver_port)}
    return render_to_response('account/settings.html', ctx, context_instance=RequestContext(request))




def run_notebook_server(request):
    """ Deprecated now -- Launces the notebook server """
    username = request.user.username
    
    # first time actions
    user_login.initialize_user_path(username)
    
    #
    u = User.objects.get(username=username)
    users =  UserProfile.objects.filter(user=u)
    if users:
        user = users[0]
    else:
        user = UserProfile.objects.create(user=u)
        user.nbserver_port = nc.NB_SERVER_PORT_BASE + int(user.user.id)
        user.nbserver_password = _get_nbserver_password()
        user.save()
    
    if os.path.exists('/proc/{0}'.format(user.nbserver_pid)): # nb server already up
        time.sleep(1)
        return HttpResponseRedirect('{0}:{1}'.format(nc.BASE_URL, user.nbserver_port))                   
    else: # first time or server not running
        ip_dir = '{0}/{1}/.ipython'.format(nc.DATA_DIR, username)
        nbserver_password_sha1 = passwd(user.nbserver_password)
        user.nbserver_pid = _run_server(ip_dir, user.nbserver_port, nbserver_password_sha1)
        user.save()            
        # sleep to let server start listening
        time.sleep(3)
        return HttpResponseRedirect('{0}:{1}'.format(nc.BASE_URL, user.nbserver_port))
        
    # show a maint msg
    return HttpResponse("<html> Server is under maintenance! Please try later.</html>")


def _run_server(ip_dir, port, password):
    """ Run a notebook server with a given ipython directory and port.
        Returns a PID.
    """
    new_env = dict(os.environ) # copy current environ
    new_env['IPYTHONDIR'] = ip_dir  # this fixes an issue
    if nc.NB_SERVER_SSL_CERT:
	pid = subprocess.Popen(['{0}python'.format(str(nc.VIRTUALENV_BIN_PATH)),
                            '{0}ipython'.format(str(nc.VIRTUALENV_BIN_PATH)),
                            'notebook',
                            '--NotebookApp.password={0}'.format(password),
                            '--NotebookApp.port={0}'.format(port),
                            '--NotebookApp.ipython_dir={0}'.format(ip_dir),
                            '--profile=nbserver', # not stable default works fine
			    '--certfile={0}'.format(nc.NB_SERVER_SSL_CERT)
                           ],
                           env=new_env).pid
    else:
        pid = subprocess.Popen(['{0}python'.format(str(nc.VIRTUALENV_BIN_PATH)),
                            '{0}ipython'.format(str(nc.VIRTUALENV_BIN_PATH)),
                            'notebook',
                            '--NotebookApp.password={0}'.format(password),
                            '--NotebookApp.port={0}'.format(port),
                            '--NotebookApp.ipython_dir={0}'.format(ip_dir),
			    '--profile=nbserver' # not stable default works fine
			   ],
			   env=new_env).pid
    return pid

def _get_nbserver_password(size=16, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))
