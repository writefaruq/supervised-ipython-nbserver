"""
Deploy IPysite app to a host 
"""
import os

from fabric.api import settings, run, env, sudo, cd, local, lcd, get, put, prompt, open_shell
from fabric.colors import green, red, yellow
from fabric.contrib.files import exists, contains, upload_template


VIRTUALENV_FOLDER = 'virtualenvs'
REPO_NAME = 'supervised-ipython-nbserver'


# hide local settings in a local_settings.py
def localenv():
    env.hosts = ['localhost', ]
    env.user = 'user'
    env.password = 'password'
    env.site_root_path = '/data/ipython'
    env.python_bin_path = '/usr/bin/python' #ensure correct version is supplied
    env.repo_url = 'https://github.com/writefaruq/%s.git' %REPO_NAME

# import local_setting by overriding above sample config
try:
    from local_settings import *
except ImportError:
    pass


# create virtualenv
def setup_virtualenv():
    """ Create a virtualenv folder and create a virtualenv named APP_NAME """
    venv_path = os.path.join(env.site_root_path, VIRTUALENV_FOLDER) 
    if not exists(venv_path):
        run("mkdir -p %s" %venv_path)
    run("virtualenv -p %s %s" %(env.python_bin_path, venv_path))

def setup_app():
    """ Checkout app code and run initial setup scripts"""
    with cd(env.site_root_path):
        run("git checkout %s" %(env.repo_url))
        run("cd %s" %REPO_NAME)
        run("pip install -r ")
     

