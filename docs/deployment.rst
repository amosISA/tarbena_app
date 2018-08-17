==========
Deployment
==========

Secret files
------------
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

django-markdown-editor (martor) app
-----------------------------------
App used to create comments related to each subvencion.
Besides, it allows you to add mentions to users with a custom query and then send them an email.

When you use in template::

    comment.contenido|safe_markdown

This has in ``Lib/site-packages/martor/extensions/mentions.py`` this code:

.. code-block:: python

        def handleMatch(self, m):
        username = self.unescape(m.group(2))

        """Makesure `username` is registered and actived."""
        if MARTOR_ENABLE_CONFIGS['mention'] == 'true':
            if username in [u.username for u in User.objects.exclude(is_active=False)]:
                url = '{0}{1}/'.format(MARTOR_MARKDOWN_BASE_MENTION_URL, username)
                el = markdown.util.etree.Element('a')
                el.set('href', url)
                el.set('class', 'direct-mention-link')
                el.text = markdown.util.AtomicString('@' + username)
                return el

If you leave it like that you will have as many duplicated queries as mentions you have in that template. So to solve this, you just have to comment this line::

    if username in [u.username for u in User.objects.exclude(is_active=False)]:

PDF (WeasyPrint)
----------------
I used this package to generate pdfs from detailed subsidies.

For installing::

    pip install WeasyPrint

.. warning::
    **Problems in Windows**:

    ``OSError: dlopen() failed to load a library: cairo / cairo-2``

    To solve this I've got to install this: `https://tschoonj.github.io/blog/2014/02/08/gtk2-64-bit-windows-runtime-environment-installer/ <https://tschoonj.github.io/blog/2014/02/08/gtk2-64-bit-windows-runtime-environment-installer/>`_

Pycairo error installation
--------------------------
When doing `pip install -r requirements/production.txt` it will give me an error: `pycairo failed building wheel`

To fix this in Linux:
::

    sudo apt-get install libcairo2-dev libjpeg-dev libgif-dev
    pip install pycairo

Mysql requirement production
----------------------------
Same as pycairo error. In Windows I install the mysql dependency from an exe but in Linux you should remove it from requirements when you install all of them and then install it by:
::

    sudo apt-get install libmysqlclient-dev