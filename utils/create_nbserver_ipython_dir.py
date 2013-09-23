import os
import shutil
import argparse


import common_settings as cs


def create_dir(initial_data_dir, ipython_dir):
    """Create the deafult dirs for Ipython Notebook servers and copy the given initial data to the notebooks folder"""
    try:
        os.mkdir(ipython_dir)
        shutil.copytree(initial_data_dir, '%s/notebooks' %ipython_dir)
    except Exception:
        raise
    print "Populated Ipython dir: %s" %ipython_dir

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create IPython dir for each Notebook server')
    parser.add_argument('--initial-data-dir', action="store", dest="initial_data_dir", default=cs.INITIAL_DATA_DIR)
    parser.add_argument('--ipython-dir', action="store", dest="ipython_dir", default="%s/%s" %(cs.USER_DATA_DIR, 'notebook-server-1'))
    
    given_args = ga = parser.parse_args()
    initial_data_dir, ipython_dir =  ga.initial_data_dir, ga.user_data_dir 
    
    create_dir(initial_data_dir, ipython_dir)