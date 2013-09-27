"""
Deploy IPysite app to a host 
"""
import os

from fabric.api import settings, run, env, sudo, cd, local, lcd, get, put, prompt, prefix, task
from fabric.colors import green, red, yellow
from fabric.contrib.files import exists, contains, upload_template
from contextlib import contextmanager
from jinja2 import Environment, FileSystemLoader

# external utils functions
from db_utils import *


# Relateive paths
VIRTUALENV_FOLDER = 'virtualenvs'
INITIAL_DATA_DIR = 'initial_data'
USER_DATA_DIR = 'user_data'
SHARED_CONFIG_DIR = 'shared_config_files'
SUPERVISORD_DIR = 'supervisord'
SUPERVISORD_CONF_DIR = os.path.join(SUPERVISORD_DIR, 'conf.d')

SHARED_CONFIG_FILE = 'all_nbserver_config.csv'
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
    # nbserver settings
    env.nbserver_id_start = 1
    env.nbserver_id_end = 100
    env.nbserver_port_base = 900  

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

################# SETUP ACTIONS ##########################

def setup_paths():
    if not exists(env.site_root_path):
        run("mkdir -p %s" %env.site_root_path)
    with cd(env.site_root_path):
        for path in [VIRTUALENV_FOLDER, INITIAL_DATA_DIR, USER_DATA_DIR,SHARED_CONFIG_DIR, SUPERVISORD_DIR, SUPERVISORD_CONF_DIR]:
            if not exists(path):
                run("mkdir -p %s" %path)


# create virtualenv
def setup_virtualenv():
    """ Create a virtualenv folder and create a virtualenv named APP_NAME """ 
    run("virtualenv -p %s %s" %(env.python_bin_path, env.venv_path))


def setup_packages():
    """ Checkout app code and run initial setup scripts"""
    with cd(env.site_root_path):
        if not exists(env.app_path):
            run("git clone %s" %(env.repo_url)) 

    with virtualenv():
        #run("easy_install -U distribute") # may be needed sometimes
        run("pip install numpy==1.7.1")  # fixes pip issue 
        run("pip install -r {0}/requirements.txt".format(env.app_path))  # install packages
    
def setup_notebook_configs():
    """Generate Notebook server and supervisord config files and paths"""
    # generate an appropriate common_settings file
    template_dir = os.path.join(os.path.curdir, 'templates')
    jinja_env = Environment(loader=FileSystemLoader(template_dir))
    template = jinja_env.get_template('common_settings.jinja.py')
    template_vars = {"host": env.hosts[0], 
                    "venv_bin_path": os.path.join(env.venv_path, 'bin'), 
                    "nbserver_id_start": env.nbserver_id_start,
                    "nbserver_id_end" : env.nbserver_id_end,
                    "nbserver_port_base": env.nbserver_post_base,
                    "initial_data_dir": os.path.join(env.site_root_path, INITIAL_DATA_DIR),
                    "user_data_dir": os.path.join(env.site_root_path, USER_DATA_DIR),
                    "supervisord_root_dir": os.path.join(env.site_root_path, SUPERVISORD_DIR),
                    "supervisord_config_dir": os.path.join(env.site_root_path, SUPERVISORD_CONF_DIR),
                    "all_nbserver_config_file": os.path.join(env.site_root_path, SHARED_CONFIG_DIR, SHARED_CONFIG_FILE),
                    "nbserver_ini_file_template": os.path.join(env.app_path, 'utils', 'nbserver_ini_file_template.ini'),
                    "supervised_nbserver_user" : env.user}
    output_from_parsed_template = template.render(template_vars)
    #print output_from_parsed_template
     
    # to save the results
    local_path = '/tmp/common_settings.py'
    with open(local_path, "wb") as fh:
        fh.write(output_from_parsed_template)
    put(local_path=local_path, remote_path=os.path.join(env.app_path, 'utils', 'common_settings.py'))
    
    # run the do-all type setup
    with virtualenv():
        run("python %s" %os.path.join(env.app_path, 'utils', 'setup_all.py'))


def setup_supervisord():
    """ Uploads supervisord config file """
    template_dir = os.path.join(os.path.curdir, 'templates')
    jinja_env = Environment(loader=FileSystemLoader(template_dir))
    template = jinja_env.get_template('supervisord.jinja.conf')
    template_vars = {"supervisord_server_addr": env.supervisord_server_addr, 
                    "supervisord_admin_username": env.supervisord_admin_username, 
                    "supervisord_admin_password": env.supervisord_admin_password,
                    "supervisord_logfile" : os.path.join(env.site_root_path, SUPERVISORD_DIR, 'supervisord.log'),
                    "supervisord_pidfile": os.path.join(env.site_root_path, SUPERVISORD_DIR, 'supervisord.pid'),
                    "supervisord_user": env.user,
                    "supervisord_ini_files": "%s/*.ini" %os.path.join(env.site_root_path, SUPERVISORD_CONF_DIR)
                    }
    output_from_parsed_template = template.render(template_vars)
    #print output_from_parsed_template
     
    # to save the results
    local_path = '/tmp/supervisord.conf'
    with open(local_path, "wb") as fh:
        fh.write(output_from_parsed_template)
    put(local_path=local_path, remote_path=os.path.join(env.site_root_path, SUPERVISORD_DIR))

def run_supervisord():
    conf_path = os.path.join(env.site_root_path, SUPERVISORD_DIR, 'supervisord.conf')
    with virtualenv():
        run("supervisord -c %s" %conf_path)

###  SETUP DJANGO APP ###################

def setup_app_config():
    # upload django local_settings file
    template_dir = os.path.join(os.path.curdir, 'templates')
    jinja_env = Environment(loader=FileSystemLoader(template_dir))
    template = jinja_env.get_template('local_settings.jinja.py')
    template_vars = {"ldap_host": env.ldap_host, 
                    "ldap_bind_dn": env.ldap_bind_dn, 
                    "ldap_bind_password": env.ldap_bind_password,
                    "ldap_search_param" : env.ldap_search_param,
                    "mysql_user": env.mysql_user,
                    "mysql_dbname": env.mysql_dbname,
                    "mysql_password": env.mysql_password,
                    "debug": env.debug
                    }
    output_from_parsed_template = template.render(template_vars)
    local_path = '/tmp/local_settings.py'
    with open(local_path, "wb") as fh:
        fh.write(output_from_parsed_template)
    put(local_path=local_path, remote_path=os.path.join(env.app_path, 'ipysite'))
    
    
    ## upload wsgi.py
    template = jinja_env.get_template('wsgi.jinja.py')
    template_vars = {"python_local_site_packages": os.path.join(env.venv_path, 'local/lib/python2.7/site-packages'), 
                    "app_path": env.app_path, 
                    "venv_path": env.venv_path
                    }
    output_from_parsed_template = template.render(template_vars)
    local_path = '/tmp/wsgi.py'
    with open(local_path, "wb") as fh:
        fh.write(output_from_parsed_template)
    put(local_path=local_path, remote_path=os.path.join(env.app_path, 'ipysite'))

def setup_app():
    # syncdb
    with virtualenv():
        run("python %s/manage.py syncdb" %env.app_path)


def setup_apache_config():
    ## upload Apache vhost config
    template_dir = os.path.join(os.path.curdir, 'templates')
    jinja_env = Environment(loader=FileSystemLoader(template_dir))
    template_vars = {"server_name": env.server_name, 
                    "app_path": env.app_path, 
                    "venv_path": env.venv_path,
                    "apache_user": env.apache_user,
                    "apache_group": env.apache_group,
                    "apache_process_count": env.apache_process_count,
                    "apache_thread_count": env.apache_thread_count,
                    }
    if env.os == 'Debian':
        template = jinja_env.get_template('wsgi_vhost_debian.jinja.conf')
    elif env.os == 'Redhat':
        template = jinja_env.get_template('wsgi_vhost_redhat.jinja.conf')
        
    output_from_parsed_template = template.render(template_vars)
    local_path = '/tmp/wsgi_vhsot.conf'
    with open(local_path, "wb") as fh:
        fh.write(output_from_parsed_template)
    
    if env.os == 'Debian':
        put(local_path=local_path, remote_path='/etc/apache2/sites-enabled')
    elif env.os == 'Redhat':
        put(local_path=local_path, remote_path='/etc/httpd/conf.d')
    

def restart_apache():
    sudo("%s restart" %env.apache_restart_cmd)