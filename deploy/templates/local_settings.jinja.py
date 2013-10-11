import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType


# LDAP Settings
AUTH_LDAP_SERVER_URI = '{{ ldap_host }}'
# This is the distinguished name (DN), the -D flag above.
AUTH_LDAP_BIND_DN = '{{ ldap_bind_dn }}'
# The bing password, the -w flag above.
AUTH_LDAP_BIND_PASSWORD = '{{ ldap_bind_password }}'
# We do lookups on a user by email so this may not work for you
# but you should get the idea. 
#AUTH_LDAP_USER_SEARCH = LDAPSearch("DC=companygroup,DC=local",
AUTH_LDAP_USER_SEARCH = LDAPSearch('{{ ldap_search_param }}',
        ldap.SCOPE_SUBTREE, "(&(objectClass=user) (cn=%(user)s) )")


# The following OPT_REFERRALS option is CRUCIAL for getting this 
# working with MS Active Directory it seems, unfortunately I have
# no idea why; it just hangs if you don't set it to 0 for us.
AUTH_LDAP_CONNECTION_OPTIONS = {
        ldap.OPT_DEBUG_LEVEL: 0,
        ldap.OPT_REFERRALS: 0,
}

AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
    "employeeid" : "employeeID",
    "Department" : "department",
}

# DB settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '{{ mysql_sock }}',
        'NAME' : '{{ mysql_dbname }}',
        'USER' : '{{ mysql_user }}',
        'PASSWORD' : '{{ mysql_password }}',
        'OPTIONS': {
        },
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '{{ logfile }}',
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers':['logfile'], # default: console
            'propagate': True,
            'level':'WARN',
        },
        'django.db.backends': {
            'handlers': ['logfile'], # default: console
            'level': 'DEBUG',
            'propagate': False,
        },
        'MYAPP': {
            'handlers': ['logfile'], # default: 'console', 'logfile'
            'level': 'DEBUG',
        },
    }
}




DEBUG = {{ debug }}