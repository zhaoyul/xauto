from fabric.api import *


def _migrate():
    local('bin/django migrate')


def _syncdb():
    local('bin/django syncdb --noinput')


def _buildout():
    local('bin/buildout -c production.cfg')


def update(syncdb=False, migrate=False, buildout=False):
    local('git pull')
    if syncdb:
    	_syncdb()
    if migrate:
    	_migrate()
    if buildout:
    	_buildout()
    local('bin/django collectstatic')
    local('supervisorctl restart xauto')
    local('supervisorctl restart xauto-photostreamer')
