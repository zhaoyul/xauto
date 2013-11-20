Installation:

1. python bootstrap.py

2. bin/buildout -c devel.cfg

3. create database (using system tools)
   - sqlite db is created automatically after syncdb call
   - postgresql using (user/name) defined in: project/settings.py

4. create database structure:
   bin/django syncdb
   bin/django migrate

5. start django application using:
   bin/django runserver


Explanation:
1. Project uses buildout to perform installation (http://buildout.org)
2. Base buildout configuration (modules/dependencies used, project's settings file name) is defined in buildout.cfg
3. For specific environments there are also.: devel.cfg, test.cfg and production.cfg which
   extend base buildout.cfg by for example using different settings file form different environments
4. In project folder there is base settings file: settings.py and settings specific for environments: development.py, test.py and production.py
   If buildout will be called with: bin/buildout -c test.cfg then bin/django command will use
   project/test.py
5. bin/django command is buildot's equivalent to manage.py. This command is generated by buildout django recipe.
   Inside this file are located all paths used by application
