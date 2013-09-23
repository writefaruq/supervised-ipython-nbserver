"""
Generate a supervisord ini file for one notebook server reading from a template ini file
"""
import os
import configparser

import common_settings as cs


def generate_ini_file(server_id, server_name, ipython_dir, nbserver_port, nbserver_sha1,
                      supervisord_ini_file_template=cs.SUPERVISORD_INI_FILE_TEMPLATE,
                      nbserver_command_template=cs.NBSERVER_CMD_TEMPATE,
                      virtualenv_bin_path=cs.VIRTUALENV_BIN_PATH,
                      output_path=cs.SUPERVISORD_CONF_DIR):
    
    print "Generating Supervisord ini file for Notebook server: %s " %server_id 

    # parse the template
    template_config = configparser.ConfigParser()
    template_config.read(supervisord_ini_file_template)

    # copy all the values to a new configparser
    nbserver_config = configparser.ConfigParser()
    section_name = "program:%s" %server_name
    nbserver_config.add_section(section_name)
    for item in template_config['program:notebook'].items():
        nbserver_config.set(section_name, item[0], item[1])    
        
    # update the template values
    command = nbserver_command_template  %(virtualenv_bin_path, virtualenv_bin_path, ipython_dir, nbserver_sha1, nbserver_port)
    nbserver_config.set(section_name, 'command', command)
    nbserver_config.set(section_name, 'process_name', server_name)
    nbserver_config.set(section_name, 'directory', virtualenv_bin_path)
    nbserver_config.set(section_name, 'priority', str(server_id))
    logfile_path = os.path.join(ipython_dir, '%s.log' %server_name)
    nbserver_config.set(section_name, 'stdout_logfile', logfile_path)
    nbserver_config.set(section_name, 'stderr_logfile', logfile_path)
    env_string = 'IPYTHONDIR={0}'.format(ipython_dir)
    nbserver_config.set(section_name, 'environment', env_string)

    #writing config
    with open('%s/%s.ini' %(output_path, server_name), 'w') as configfile:    # save config
        nbserver_config.write(configfile)


if __name__ == '__main__':
    server_id = 1 
    server_name = 'notebook-server-1'
    ipython_dir = '/ipython/dir'
    nbserver_port = 1001
    nbserver_sha1 = 'xhcvxzzvnzxvnklxzvjlxzdvjl'
    output_path = '/tmp/ipython'
    generate_ini_file(server_id=server_id, server_name=server_name, ipython_dir=ipython_dir, 
                      nbserver_port=nbserver_port, nbserver_sha1=nbserver_sha1, output_path=output_path)