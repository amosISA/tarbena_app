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
Created Login and Signup system in the root project (urls.py, templates, static).

Profiles
^^^^^^^^
When a new user is created, his profile is also created.

Subvenciones
^^^^^^^^^^^^
| Application to manage subsidies.
| Tables:

- Estado
- Colectivo
- Ente
- Area
- Subvencion
- Comment
- Like

Create Subvencion
"""""""""""""""""
| When I create a new subsidie I add admin functionality in my form so I can add new fields suchs as: estado. Its a Django Popup functionality:
| `django-admin-popup-functionality <https://stackoverflow.com/questions/2347582/django-admin-popup-functionality>`_


| On the other hand, I insert the comment field into the subvencion form with a formset following this guide:
| `django formset implementation <http://pythonpiura.org/posts/implementando-django-formsets/>`_


| Here for the formset field (contenido) I used markdown editor (added his configuration into settings):
| `Django markdown editor <https://github.com/agusmakmun/django-markdown-editor>`_

In my custom template the editor didnt't work as expected so in my base.html I had to add the following urls::

    <link href="{% static 'plugins/css/ace.min.css' %}" type="text/css" media="all" rel="stylesheet" />
    <link href="{% static 'plugins/css/semantic.min.css' %}" type="text/css" media="all" rel="stylesheet" />
    <link href="{% static 'plugins/css/resizable.min.css' %}" type="text/css" media="all" rel="stylesheet" />
    <link href="{% static 'martor/css/martor.min.css' %}" type="text/css" media="all" rel="stylesheet" />
    <script type="text/javascript" src="{% static 'plugins/js/ace.js' %}"></script>
    <script type="text/javascript" src="{% static 'plugins/js/semantic.min.js' %}"></script>
    <script type="text/javascript" src="{% static 'plugins/js/mode-markdown.js' %}"></script>
    <script type="text/javascript" src="{% static 'plugins/js/ext-language_tools.js' %}"></script>
    <script type="text/javascript" src="{% static 'plugins/js/theme-github.js' %}"></script>
    <script type="text/javascript" src="{% static 'plugins/js/highlight.min.js' %}"></script>
    <script type="text/javascript" src="{% static 'plugins/js/resizable.min.js' %}"></script>
    <script type="text/javascript" src="{% static 'plugins/js/emojis.min.js' %}"></script>
    <script type="text/javascript" src="{% static 'martor/js/martor.min.js' %}"></script>



| Also I follow this guide to add the dropdown functionality for ente and area:
| `Dependent dropdown list <https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html>`_

| Datatables functionality to list subvenciones into the index.html


Parcelas
^^^^^^^^

Django Honeypot
^^^^^^^^^^^^^^^
`https://github.com/jamesturk/django-honeypot <https://github.com/jamesturk/django-honeypot>`_

Django Admin Interface
^^^^^^^^^^^^^^^^^^^^^^
| `https://djangopackages.org/grids/g/admin-styling/ <https://djangopackages.org/grids/g/admin-styling/>`_
| `https://github.com/fabiocaccamo/django-admin-interface <https://github.com/fabiocaccamo/django-admin-interface>`_
| You can choose your own theme!

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