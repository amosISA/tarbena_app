==========
Celery
==========
Everything you execute in a view will affect response time. In many situations
you might want to return a response to the user as quickly as possible and let the
server execute some process asynchronously.

One example is sending e-mails to users. If your site sends
e-mail notifications from a view, the SMTP connection might fail or slow down the
response. Launching asynchronous tasks is essential to avoid blocking execution.

Installation
------------
::

    pip install celery==3.1.18

.. note::
    Celery requires a `message broker` in order to handle requests from an external
    source. The broker takes care of sending messages to Celery `workers`, which
    process tasks as they receive them. Let's install a message broker.

Message Broker: RabbitMQ or Redis
---------------------------------

There are several options to choose as a message broker for Celery, including
key-value stores such as Redis or an actual message system such as RabbitMQ. We will
configure Celery with RabbitMQ, since it's a recommended message worker for Celery.

| If you are using Linux, you can install RabbitMQ from the shell using the following command

::

    apt-get install rabbitmq

If you need to install RabbitMQ on Mac OS X or Windows, you can find standalone
versions at `https://www.rabbitmq.com/download.html <https://www.rabbitmq.com/download.html>`_
.

First you need to download and install erlang: `http://www.erlang.org/downloads <http://www.erlang.org/downloads>`_

After installing it, launch RabbitMQ using the following command from the shell::

    rabbitmq-server

You will see an output that ends with the following line::

    Starting broker... completed with 10 plugins.

RabbitMQ is running and ready to receive messages.

Adding Celery to my project
---------------------------
You have to provide a configuration for the Celery instance. Create a new file next
to the `settings.py` name it `celery.py`. This file will contain the
Celery configuration for your project.

Now you can add asynchronous tasks to your project.

Monitoring Celery
-----------------
You might want to monitor the asynchronous tasks that are executed. Flower is a
web-based tool for monitoring Celery. You can install Flower using the command
::

    pip install flower

Once installed, you can launch Flower running the following command from your
project directory::

    celery -A config flower

Open http://localhost:5555/dashboard in your browser. You will be able to see
the active Celery workers and asynchronous tasks' statistics.
The above command will tell you the tasks you have.

| Another command for check if the tasks are successfully launched is.

::

    celery -A config worker -l info

Things I have created:

- celery.py # in my config folder
- tasks.py # in the app you want to run tasks
- then in views you define that task
