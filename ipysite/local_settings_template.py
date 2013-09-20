""" 
Hide your local_settings here
"""

import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType



AUTH_LDAP_SERVER_URI = "ldap://<URL>"
# This is the distinguished name (DN), the -D flag above.
AUTH_LDAP_BIND_DN = ''
# The bing password, the -w flag above.
AUTH_LDAP_BIND_PASSWORD = ''

# We do lookups on a user by email so this may not work for you
# but you should get the idea. 
AUTH_LDAP_USER_SEARCH = LDAPSearch("DC=companygroup,DC=local",
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

