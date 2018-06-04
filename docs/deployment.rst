============
Secret files
============
| When deploying don't save the secret files into the project. Save them into a safe place and ignore them with gitignore. Things such as: database password, ``SECRET_KEY``, email password, etc.

When I use::

    install -r requirements/production.txt

Check that in base.txt I have no debug toolbar and it's in local.txt and also check that I have everything from development server with::

    pip freeze -r requirements/base.txt

Notify app
----------
Override verb character limit to TextField::

    # Lib/site-packages/notify/models.py
    verb = models.TextField(verbose_name=_('Verb of the action'))
    python manage.py makemigrations
    python manage.py migrate

Martor (markdown) app
---------------------
Override mention href::

     # Lib/site-packages/martor/extensions/mention.py
