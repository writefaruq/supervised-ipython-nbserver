"""
Holds the commons settings between django application ipysite and supervisord
"""
import time

NOW = time.strftime("%Y%m%d%H%M", time.gmtime())


# Adjust these configs
HOSTNAME = '{{ host }}'
VIRTUALENV_BIN_PATH = '{{ venv_bin_path }}' 

# The following needs tweaking and setup
NB_SERVER_ID_START = '{{ nbserver_id_start }}'
NB_SERVER_ID_END = '{{ nbserver_id_end }}'
NB_SERVER_PORT_BASE = '{{ nbserver_port_base}}'

INITIAL_DATA_DIR = '{{ initial_data_dir }}'
USER_DATA_DIR = '{{ user_data_dir }}'


SUPERVISORD_CONF_DIR = '{{ supervisord_config_dir }}'
ALL_NBSERVER_CONFIG_FILE = '{{ all_nbserver_config_file }}'
SUPERVISORD_INI_FILE_TEMPLATE = '{{ nbserver_ini_file_template }}'

# The following entries usually won't need any change
USER_PASSWORD_LENGTH = 16
NBSERVER_NAME_FORMAT = 'notebook-server-%d'
NBSERVER_CMD_TEMPATE = "%s/python %s/ipython notebook  --NotebookApp.ipython_dir=%s  --NotebookApp.open_browser=False --NotebookApp.ip=%s --NotebookApp.password=%s --NotebookApp.port=%s --IPKernelApp.pylab=inline --NotebookApp.enable_mathjax=True"

# config file entries
NBSERVER_ALL_CONFIG_ID_COLUMN = 0
NBSERVER_ALL_CONFIG_SERVER_NAME_COLUMN = 1
NBSERVER_ALL_CONFIG_IPYTHON_DIR_COLUMN = 2
NBSERVER_ALL_CONFIG_PORT_COLUMN = 3
NBSERVER_ALL_CONFIG_SHA_COLUMN = 4
NBSERVER_ALL_CONFIG_PASSWORD_COLUMN = 5