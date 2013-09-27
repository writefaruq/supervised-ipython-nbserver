import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('{{ python_local_site_packages }}') #/path/to/virtualenv/local/lib/python2.7/site-packages

# Add the app's directory to the PYTHONPATH
sys.path.append('{{ app_path }}')
sys.path.append(os.path.join('{{ app_path }}', 'settings.py'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'ipysite.settings'

# Activate your virtual env
activate_env=os.path.expanduser(os.path.join('{{ venv_path }}', 'bin/activate_this.py'))
execfile(activate_env, dict(__file__=activate_env))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()