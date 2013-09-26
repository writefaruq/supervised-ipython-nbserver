"""
Holds the commons settings between django application ipysite and supervisord
"""
import time

NOW = time.strftime("%Y%m%d%H%M", time.gmtime())
HOSTNAME = 'localhost'

# The following needs tweaking and setup
ALL_NBSERVER_CONFIG_FILE = '../shared_config_files/all_nbserver_config_%s.csv' %NOW # Holds all nbserver configs, shared between supervisord and django application
NB_SERVER_ID_START = 1
NB_SERVER_ID_END = 100
NB_SERVER_PORT_BASE = 9000

INITIAL_DATA_DIR = '/data/ipython/initial_data/'
USER_DATA_DIR = '/data/ipython/user_data/'

# Adjust Notebook server config
VIRTUALENV_BIN_PATH = '/home/faruq/projects/venvs/sipnb/bin' 
SUPERVISORD_CONF_DIR = '../supervisord_config_files/conf.d'


# The following entries usually won't need any change
USER_PASSWORD_LENGTH = 16
NBSERVER_NAME_FORMAT = 'notebook-server-%d'
SUPERVISORD_INI_FILE_TEMPLATE = 'nbserver_ini_file_template.ini'
NBSERVER_CMD_TEMPATE = "%s/python %s/ipython notebook  --NotebookApp.ipython_dir=%s  --NotebookApp.open_browser=False --NotebookApp.ip=%s --NotebookApp.password=%s --NotebookApp.port=%s --IPKernelApp.pylab=inline --NotebookApp.enable_mathjax=True"

# config file entries
NBSERVER_ALL_CONFIG_ID_COLUMN = 0
NBSERVER_ALL_CONFIG_SERVER_NAME_COLUMN = 1
NBSERVER_ALL_CONFIG_IPYTHON_DIR_COLUMN = 2
NBSERVER_ALL_CONFIG_PORT_COLUMN = 3
NBSERVER_ALL_CONFIG_SHA_COLUMN = 4
NBSERVER_ALL_CONFIG_PASSWORD_COLUMN = 5
