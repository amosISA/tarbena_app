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

Steps to deploy
---------------
1. In Ubuntu I can't install Mysql by my requirements file with the command. So I install this package first:
::

    sudo apt-get install libmysqlclient-dev
    # Then I can do:
    pip install mysqlclient

2. Production settings I use:
::

    'PASSWORD': os.getenv('MYSQL_PASSWORD'),

    # Then I use this command:
    export MYSQL_PASSWORD=asdasdasd23423

    # So it gets the password from here
    # Show all exported variables:
    export -p

    # Or search by one:
    export -p | grep myvariable

    # Delete an exported variable:
    unset myvariable

.. warning::
    This has an error and is that when you turn off your command line the variables gets deleted so you can save them into a secrete         file into your server and get the info from there.

3. WeasyPrint error:
::

    OSError: cannot load library 'pango-1.0': pango-1.0: cannot open shared object file: No such file or directory.  Additionally, ctypes.util.find_library() did not manage to locate a library called 'pango-1.0'

    # With this error you just have to install:
    apt-get install pango1.0-tests

4. The wsgi.py file:
In python2 the execfile function works but in python3 it does not so you have to replace:
::

    # This:
    execfile(activate_this, dict(__file__=activate_this)) # py2

    # For:
    exec(open(activate_this).read()) #py3

5. In administration panel add SITES_ID: 1 (development) and 2 (production)

6. Add logging to production so you can debug in production server

7. Settings file. I create a dir named settings and inside of him I make him module by creating `__init__.py`. And inside that y import them. And I create each file for each environment but I ignore the local one so that in production it gets only the production file.

8. You can check your deployment and if you are using Apache you can check ur syntax:
::

    python3 manage.py check --deploy
    sudo apache2ctl configtest

9. Celery. In production server I need celery to run my tasks on the background. More info in my deploy file.

Celery
------
Now we have intstalled with pip in our project celery so its time to start it.
Nice guides:

`https://www.digitalocean.com/community/tutorials/how-to-use-celery-with-rabbitmq-to-queue-tasks-on-an-ubuntu-vps <https://www.digitalocean.com/community/tutorials/how-to-use-celery-with-rabbitmq-to-queue-tasks-on-an-ubuntu-vps>`_


`https://thomassileo.name/blog/2012/08/20/how-to-keep-celery-running-with-supervisor/ <https://thomassileo.name/blog/2012/08/20/how-to-keep-celery-running-with-supervisor/>`_


| We will include a "&" character at the end of our string to put our worker process in the background:

::

    celery worker -A config &
    celery -A config worker -l info

    # This if I restart the server or if I close the server console by ssh stops working.
    # So that I need a python program to keep runing celery in the background (supervisor).

Keep in mind that I can't start celery as superadmin so I create a new user:
::

    sudo adduser celery
    whoami
    # swap to new user
    su - celery
    # swap back to root
    su -

    # Giver superadmin permissions to new user
    visudo
    # I need to be superuser to modify this doc
    # So after my root user I put celery and the same permissions as root

    $ pip install supervisor # python 2
    $ pip install git+https://github.com/Supervisor/supervisor # python 3
    $ cd /path/to/your/project
    $ echo_supervisord_conf > supervisord.conf

    # Now swap back to celery user and go to my root project and activate my virtualenv
    # Then run this command inside:
    supervisord

    # Next, just add this section after the [supervisord] section:
    [program:celeryd]
    command=/home/thomas/virtualenvs/yourvenv/bin/celery worker --app=myapp -l info
    stdout_logfile=/path/to/your/logs/celeryd.log
    stderr_logfile=/path/to/your/logs/celeryd.log
    autostart=true
    autorestart=true
    startsecs=10
    stopwaitsecs=600

But this does not seem to work on the background with &, so I tried this new guide that works like a charm.

| `Guide I followed. <https://realpython.com/asynchronous-tasks-with-django-and-celery/#running-remotely>`_

::

    sudo apt-get install supervisor

In the root project create a folder called supervisor and inside create the two following files:
| **subvenciones_celery.conf**
::

    ; ==================================
    ;  celery worker supervisor example
    ; ==================================

    ; the name of your supervisord program
    [program:configcelery]

    ; Set full path to celery program if using virtualenv
    command=/home/admin/tarbena/bin/celery worker -A config --loglevel=INFO

    ; The directory to your Django project
    directory=/home/admin/tarbena

    ; If supervisord is run as the root user, switch users to this UNIX user account
    ; before doing any processing.
    user=amos

    ; Supervisor will start as many instances of this program as named by numprocs
    numprocs=1

    ; Put process stdout output in this file
    stdout_logfile=/var/log/celery/subvenciones_worker.log

    ; Put process stderr output in this file
    stderr_logfile=/var/log/celery/subvenciones_worker.log

    ; If true, this program will start automatically when supervisord is started
    autostart=true

    ; May be one of false, unexpected, or true. If false, the process will never
    ; be autorestarted. If unexpected, the process will be restart when the program
    ; exits with an exit code that is not one of the exit codes associated with this
    ; process’ configuration (see exitcodes). If true, the process will be
    ; unconditionally restarted when it exits, without regard to its exit code.
    autorestart=true

    ; The total number of seconds which the program needs to stay running after
    ; a startup to consider the start successful.
    startsecs=10

    ; Need to wait for currently executing tasks to finish at shutdown.
    ; Increase this if you have very long running tasks.

| **subvenciones_celerybeat.conf**

::

    ================================
    ;  celery beat supervisor example
    ; ================================

    ; the name of your supervisord program
    [program:configcelerybeat]

    ; Set full path to celery program if using virtualenv
    command=/home/admin/tarbena/bin/celerybeat -A config --loglevel=INFO

    ; The directory to your Django project
    directory=/home/admin/tarbena/src

    ; If supervisord is run as the root user, switch users to this UNIX user account
    ; before doing any processing.
    user=amos

    ; Supervisor will start as many instances of this program as named by numprocs
    numprocs=1

    ; Put process stdout output in this file
    stdout_logfile=/var/log/celery/subvenciones_beat.log

    ; Put process stderr output in this file
    stderr_logfile=/var/log/celery/subvenciones_beat.log

    ; If true, this program will start automatically when supervisord is started
    autostart=true

    ; May be one of false, unexpected, or true. If false, the process will never
    ; be autorestarted. If unexpected, the process will be restart when the program
    ; exits with an exit code that is not one of the exit codes associated with this
    ; process’ configuration (see exitcodes). If true, the process will be
    ; unconditionally restarted when it exits, without regard to its exit code.
    autorestart=true

    ; The total number of seconds which the program needs to stay running after
    ; a startup to consider the start successful.
    startsecs=10

    ; if your broker is supervised, set its priority higher
    ; so it starts first
    priority=999

Then create the logs in `/var/log`.
Now just copy these files to the remote server in the `/etc/supervisor/conf.d/` directory.
Then:

::

    $ sudo supervisorctl reread
    $ sudo supervisorctl update

    $ sudo supervisorctl stop configcelery
    $ sudo supervisorctl start configcelery
    $ sudo supervisorctl status configcelery

The default Celery scheduler creates some files to store its schedule locally. These files would be `celerybeat-schedule.db` and `celerybeat.pid`. If you are using a version control system like Git (which you should!), it is a good idea to ignore this files and not add them to your repository since they are for running processes locally.


Varnish Cache
-------------------
HTTP accelerator designed for content-heavy dynamic web sites as well as APIs. So that make our web faster.