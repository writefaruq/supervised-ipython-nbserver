import os
import shutil

from django.db import models
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from jinja2 import Environment, FileSystemLoader

from ipysite.models import UserProfile 
import ipysite.notebook_config as nc


def initialize_user_path(username):
    """ 
    Does the first time login actions.
    - Create a personalized folder in IPYTHON/USER_DATA path
    - Upload a personalized Notebook server config file
    - Copy Initial notebook files to the server's working path
    """
    if not os.path.exists('{0}/{1}'.format(nc.DATA_DIR, username)):
        user_dir = '{0}/{1}'.format(nc.DATA_DIR, username)
        ip_dir = '{0}/.ipython'.format(user_dir)
        conf_dir = '{0}/profile_nbserver'.format(ip_dir)
        nb_dir = '{0}/notebooks'.format(user_dir)
        
        os.makedirs(ip_dir)
        os.makedirs(conf_dir)
        
        # render config
        env = Environment(loader=FileSystemLoader(nc.NB_SERVER_CONFIG_TEMPLATE_DIR))
        template = env.get_template('ipython_notebook_config.jinja.py')
        template_vars = {"username": username, 
                         "ip_dir": ip_dir, 
                         "nb_dir": nb_dir}
        output_from_parsed_template = template.render(template_vars)
        
     
        # to save the results
        config_path = '{0}/ipython_notebook_config.py'.format(conf_dir)
        with open(config_path, "wb") as fh:
            fh.write(output_from_parsed_template)

        # copy data files over
        if nc.INITDATA_DIR:
            shutil.copytree(nc.INITDATA_DIR, '{0}'.format(nb_dir))
        else:
            os.makedirs(nb_dir)
