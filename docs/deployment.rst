============
Secret files
============
When deploying don't save the secret files into the project. Save them into a safe place and ignore them with gitignore.
Thigs such as: database password, SECRET_KEY, email password, etc.

When I use:
install -r requirements/production.txt
Check that in base.txt I have no debug toolbar and its in local.txt and also check that I have everyting from development server with:
pip freeze -r requirements/base.txt