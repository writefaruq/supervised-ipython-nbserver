"""
Deploy IPysite app to a host 
"""
import os

from fabric.api import settings, run, env, sudo, cd, local, lcd, get, put, prompt, prefix, task
from fabric.colors import green, red, yellow
from fabric.contrib.files import exists, contains, upload_template
from contextlib import contextmanager


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
    env.venv_path = os.path.join(env.site_root_path, VIRTUALENV_FOLDER, REPO_NAME)
    env.app_path = os.path.join(env.site_root_path, REPO_NAME)

# import local_setting by overriding above sample config
try:
    from local_settings import *
except ImportError:
    pass


@contextmanager
def virtualenv():
    """
    Runs commands within the project's virtualenv.
    """
    with prefix("source %s/bin/activate" % env.venv_path):
        yield


# create virtualenv
def setup_virtualenv():
    """ Create a virtualenv folder and create a virtualenv named APP_NAME """ 
    if not exists(env.venv_path):
        run("mkdir -p %s" %env.venv_path)
    run("virtualenv -p %s %s" %(env.python_bin_path, env.venv_path))


def setup_packages():
    """ Checkout app code and run initial setup scripts"""
    with cd(env.site_root_path):
        if not exists(env.app_path):
            run("git clone %s" %(env.repo_url)) 

    with virtualenv():
        run("easy_install -U distribute")
        run("pip install -r {0}/requirements.txt".format(env.app_path))  # install packages
    
def setup_notebook_configs():
    """Generate Notebook server and supervisord config files and paths"""
    with cd(env.app_path):
        with virtualenv():
            run("python ipysite/utils/setup_all.py")
            


     

