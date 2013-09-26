"""
Deploy IPysite app to a host 
"""
import os

from fabric.api import settings, run, env, sudo, cd, local, lcd, get, put, prompt, open_shell
from fabric.colors import green, red, yellow
from fabric.contrib.files import exists, contains, upload_template


VIRTUALENV_FOLDER = 'virtualenvs'


# hide local settings in a local_settings.py
def localenv():
    env.hosts = ['localhost', ]
    env.user = 'user'
    env.password = 'password'
    env.site_root_path = '/data/ipython'
    env.python_bin_path = '/usr/bin/python' #ensure correct version is supplied
    env.repo_url = '' 

# import local_setting by overriding above sample config
try:
    from local_settings import *
except ImportError:
    pass

# some common stuff


# create virtualenv
def setup_virtualenv():
    """ Create a virtualenv folder and create a virtualenv named APP_NAME """
    venv_path = os.path.join(env.site_root_path, VIRTUALENV_FOLDER) 
    if not exists(venv_path):
        run("mkdir -p %s" %venv_path)
    run("virtualenv -p %s %s" %(env.python_bin_path, venv_path))

