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

# Export my production database password and then get it or save it in a secure folder in the production server
```
export MYSQL_PASSWORD=1234
'PASSWORD': os.getenv('MYSQL_PASSWORD'),
Or I can add it to my file and import it like the secret key and the email password.
```

# Save my SECREY_KEY in a secure file in the production server
```
>>> from django.core.signing import Signer
>>> signer = Signer()
>>> value = signer.sign('My string')
>>> value
'My string:GdMGD6HNQ_qdgxYP8yBZAdAIV1w'
```

# Multiple requirements files
## base.txt
Place the dependencies used in all environments

## local.txt
Place the dependencies used in local environment such as debug toolbar

## ci.txt => continuous integration
The needs of a continuous integration such as django-jenkins or coverage

## production.txt
Place the dependencies used in production environment

# Installing From Multiple Requirements Files
```
pip install -r requirements/local.txt
pip install -r requirements/production.txt
```

# New theme to backend - Django Admin Interface
https://djangopackages.org/grids/g/admin-styling/
https://github.com/fabiocaccamo/django-admin-interface
You can choose your own theme!

# Django honeypot
https://github.com/dmpayton/django-admin-honeypot
If someone try to use my admin site It will send me information about him because its a fake url admin site

# Admindocs to my admin django so I can list all my models and see everythings
https://docs.djangoproject.com/en/1.11/ref/contrib/admin/admindocs/
```
pip install docutils
```