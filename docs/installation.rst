Introduction
============

About the app
-------------

| Each Town Hall in small towns needs to be introduced to new technologies. So for my people (Tárbena/Alicante)
| I have decided to make an application that suits their needs.

| The sole purpose of ``django-notify-x`` is to add a *facebook-like* notification system functionality and give you the ability to control | everything.

**The key features of Tarbena apps are**:

    - Manage subsidies
    - Manage parcels
    - Manage keys that belongs to the Town Hall of Tarbena
    - Add any other app they think can resolve their daily problems

Requirements
------------
1. Django 1.11.6
2. Python 3.6.5
3. mysqlclient

Get ready (Windows)
---------
- Download `python <https://www.python.org/downloads/>`_
- Install pip. For windows we get it `here <https://bootstrap.pypa.io/get-pip.py>`_
- Create an environment variable for pip::

    setx PATH "%PATH%;C:\Python27\Scripts"

- Create an isolated environment for python with virtualenv::

    pip install virtualenvwrapper-win
    mkvirtualenv myproject

- Activate the virtualenv::

    Scripts/activate => windows
    source bin/activate => linux

- Install Django with pip
- Install MySQL::

    For Python 2.7:
    Download it here: http://www.codegood.com/download/10/
    And with our virtualenv activated we do: easy_install file://C:/Users/ORDENADOR_1/Downloads/MySQL-python-1.2.3.win32-py2.7.exe

    For Python 3.6:
    Download it here: https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysql-python
    32 bits refers to Python version and not to our system

- Create Django project and migrate the database::

    django-admin startproject src
    python manage.py migrate
    python manage.py startapp subvenciones