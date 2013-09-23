""" 
Shortcut script to run the whole process at once:
1. Generate all Notebook server config
2. Create each Notebook server's IPYthon dir based on the generated config file in #1
3. Generate Supervisord ini file (based on #1) for each Notebook server so that supervisord can launch them
"""
import csv

import common_settings as cs
from generate_all_nbserver_config import generate_config
from create_nbserver_ipython_dir import create_dir
from generate_supervisord_ini_file import generate_ini_file


def main(out_file=cs.ALL_NBSERVER_CONFIG_FILE, 
         nbserver_id_start=cs.NB_SERVER_ID_START, 
         nbserver_id_end=cs.NB_SERVER_ID_END, 
         nbserver_port_base=cs.NB_SERVER_PORT_BASE,
         initial_data_dir=cs.INITIAL_DATA_DIR,
         output_path=cs.SUPERVISORD_CONF_DIR
         ): 
    
    #generate all nbserver configs
    generate_config(out_file, nbserver_id_start, nbserver_id_end, nbserver_port_base)
    
    # read the all_config  file and create IPython dirs and supervisor ini files
    config_file = open(cs.ALL_NBSERVER_CONFIG_FILE, 'r')
    reader = csv.reader(config_file)
    for row in reader:
        server_name = row[cs.NBSERVER_ALL_CONFIG_SERVER_NAME_COLUMN]
        ipython_dir = row[cs.NBSERVER_ALL_CONFIG_IPYTHON_DIR_COLUMN] 
        # createIPython dirs
        create_dir(initial_data_dir, ipython_dir)
        # Generate supervisord ini files
        server_id = row[cs.NBSERVER_ALL_CONFIG_ID_COLUMN]
        ipython_dir = row[cs.NBSERVER_ALL_CONFIG_IPYTHON_DIR_COLUMN]
        nbserver_port = row[cs.NBSERVER_ALL_CONFIG_PORT_COLUMN]
        nbserver_sha =  row[cs.NBSERVER_ALL_CONFIG_SHA_COLUMN]
        generate_ini_file(server_id=server_id, server_name=server_name, ipython_dir=ipython_dir, 
                      nbserver_port=nbserver_port, nbserver_sha1=nbserver_sha, output_path=output_path)


if __name__ == '__main__':
    main()