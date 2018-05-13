May 2018: Starting Tárbena project 
==================================

Preparing project configuration
-------------------------------
1. Gitignore: local settings 
2. Creating settings module with files for different environments: base, local and production 
3. Creating project documentation with reStructuredText(.rst) files and Sphinx
4. Multiple requirements files

Apps
----
- **Authentication** (built-in django.auth): This app handles user signups, login, and logout
- **Profiles**: this app provides additional user profile information
- **Subvenciones**: subsidies management
- **Parcelas**: parcels management with Google Maps
- **Django Honeypot**: admin security
- **Django Admin Interface**: theme for Django Admin Panel

Authentication
^^^^^^^^^^^^^^

Profiles
^^^^^^^^
When a new user is crwated, his profile is also created.

Subvenciones
^^^^^^^^^^^^

Parcelas
^^^^^^^^

Django Honeypot
^^^^^^^^^^^^^^^
`https://github.com/jamesturk/django-honeypot <https://github.com/jamesturk/django-honeypot>`_

Django Admin Interface
^^^^^^^^^^^^^^^^^^^^^^
`https://djangopackages.org/grids/g/admin-styling/ <https://djangopackages.org/grids/g/admin-styling/>`_
`https://github.com/fabiocaccamo/django-admin-interface <https://github.com/fabiocaccamo/django-admin-interface>`_
You can choose your own theme!

Project commands
----------------
To start the Python interactive interpreter with Django, using your settings/local.py settings file::

    python manage.py shell --settings=tarbena.settings.local

To run the local development server with your settings/local.py settings file::

    python manage.py runserver --settings=tarbena.settings.local

Backup my models::

    python manage.py dumpdata myapp --indent=2 --output=myapp/fixtures/subsidies.json
    python manage.py dumpdata auth --indent=2 --output=myapp/fixtures/auth.json

Load data from those backups::

    python .\manage.py loaddata subsidies.json

Export my production database password and then get it or save it in a secure folder in the production server::

    export MYSQL_PASSWORD=1234
    'PASSWORD': os.getenv('MYSQL_PASSWORD'),
    Or I can add it to my file and import it like the secret key and the email password.



Save my SECREY_KEY in a secure file in the production server::

    >>> from django.core.signing import Signer
    >>> signer = Signer()
    >>> value = signer.sign('My string')
    >>> value
    'My string:GdMGD6HNQ_qdgxYP8yBZAdAIV1w'

Multiple requirements files
---------------------------
- **base.txt**: place the dependencies used in all environments
- **local.txt**: place the dependencies used in local environment such as debug toolbar
- **production.txt**: place the dependencies used in production environment
- **ci.txt** (continuous integration): the needs of a continuous integration such as django-jenkins or coverage

Admin Documentation
-------------------
`https://docs.djangoproject.com/en/1.11/ref/contrib/admin/admindocs/ <https://docs.djangoproject.com/en/1.11/ref/contrib/admin/admindocs/>`_
::

    pip install docutils

