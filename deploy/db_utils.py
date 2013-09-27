from fabric.api import settings, run, env, sudo, cd, local, lcd, get, put, prompt, prefix, task


def empty_db():
    """ Empty all tables of a given DB """
    db_name = prompt("Enter DB name to empty:")
    cmd = """
    (echo 'SET foreign_key_checks = 0;'; 
    (mysqldump -u%s -p%s --add-drop-table --no-data %s | 
     grep ^DROP); 
     echo 'SET foreign_key_checks = 1;') | \
     mysql -u%s -p%s -b %s
    """ %(env.mysql_user, env.mysql_password, db_name, env.mysql_user, env.mysql_password, db_name)
    run(cmd) 

def show_dbs():
    """ Wraps mysql show databases cmd"""
    q = "show databases"
    run("echo '%s' | mysql -u%s -p%s" %(q, env.mysql_user, env.mysql_password))


def ls_db():
    """ List a dbs with size in MB """
    dbname = prompt("Which DB to ls?")
    q = """SELECT table_schema                                        "DB Name", 
       Round(Sum(data_length + index_length) / 1024 / 1024, 1) "DB Size in MB" 
        FROM   information_schema.tables         
        WHERE table_schema = \"%s\" 
        GROUP  BY table_schema """ %dbname
    run("echo '%s' | mysql -u%s -p%s" %(q, env.mysql_user, env.mysql_password))
