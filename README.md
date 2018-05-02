# To start the Python interactive interpreter with Django, using your settings/local.py settings file:
```
python manage.py shell --settings=tarbena.settings.local
```

# To run the local development server with your settings/local.py settings file:
```
python manage.py runserver --settings=tarbena.settings.local
```

# Backup my models
```
python manage.py dumpdata myapp --indent=2 --output=myapp/fixtures/subsidies.json
python manage.py dumpdata auth --indent=2 --output=myapp/fixtures/auth.json
```

# Load data from those backups
```
python .\manage.py loaddata subsidies.json
```