import argparse
import os
import csv
import random
import string
from IPython.lib import passwd

import common_settings as cs

def _get_nbserver_password(size=cs.USER_PASSWORD_LENGTH, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def generate_entry(server_id, server_port_base, server_name_format=cs.NBSERVER_NAME_FORMAT, USER_DATA_DIR=cs.USER_DATA_DIR):
    """ Creates a config entry for each notebook instance
    [notebook-server-<ID>, USER_DATA_DIR/ipython_dir,  port, sha1, password]
    
    """
    txt_password = _get_nbserver_password()
    sha1 = passwd(txt_password)
    server_name =  server_name_format %server_id
    ipython_dir = os.path.join(USER_DATA_DIR, server_name)
    entry = [server_id, server_name, ipython_dir, server_port_base + server_id, sha1, txt_password]
    return entry

def generate_config(out_file, nbserver_id_start, nbserver_id_end, nbserver_port_base):
    """ Generate CSV file containing all Notebook Server config settings"""
    config_outfile = open(out_file, 'wb')
    csv_writer = csv.writer(config_outfile)    
    for server_id in xrange(nbserver_id_start, nbserver_id_end + 1):
        row = generate_entry(server_id, nbserver_port_base)
        csv_writer.writerow(row)
    print "Generated all Notebook Server config settings in %s" %out_file


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate All Notebook Server Config')
    parser.add_argument('--out-file', action="store", dest="out_file", default=cs.ALL_NBSERVER_CONFIG_FILE)
    parser.add_argument('--nbserver-id-start', action="store", dest="nbserver_id_start", default=cs.NB_SERVER_ID_START, type=int)
    parser.add_argument('--nbserver-id-end', action="store", dest="nbserver_id_end", default=cs.NB_SERVER_ID_END, type=int)
    parser.add_argument('--nbserver-port-base', action="store", dest="nbserver_port_base", default=cs.NB_SERVER_PORT_BASE)
    
    given_args = ga = parser.parse_args()
    out_file, nbserver_id_start = ga.out_file, ga.nbserver_id_start  
    nbserver_id_end, nbserver_port_base = ga.nbserver_id_end, ga.nbserver_port_base 
    
    generate_config(out_file, nbserver_id_start, nbserver_id_end, nbserver_port_base)