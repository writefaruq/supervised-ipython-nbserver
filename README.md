Supervised IPython Notebook Server
===================================

This project implements a highly secure and scalable IPython Notebook service to facilitate accessing IPython notebook servers from a browser. This is designed for teaching courses where
large number of students can practise data-driven computing exercises in their browser without installing any Python packages on their machines.    


Features
---------

- Separte Notebook server process management via Supervisor package unlike forking Notebook servers via the Apache process.
- Integrated with LDAP authentication.
- All Notebook servers are password-protected to prevent illegeal access.
- Course/site administrators can control the access to the Notebook servers. Only authorized users can access the Notebook servers.
- Mass user authorization based on CSV file uploads.
- Automatic deployment option in a virtual environment via Fabric package.



Getting Started
----------------
    pip install virtualenv
    virtualenv mysiteenv
    source mysiteenv/bin/activate
    pip install -r requirements.txt
    python manage.py syncdb
    python manage.py runserver


Contact
--------
M Omar Faruque Sarker
writefaruq[at]gmail.com



