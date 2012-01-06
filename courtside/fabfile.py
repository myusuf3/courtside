from __future__ import with_statement
from fabric.api import local, settings, abort
from fabric.contrib.console import confirm

def test():
	with settings(warn_only=True):
		result = local("./manage.py test game", capture=True)
	if result.failed and not confirm("Tests failed. Continue anyway?"):
		abort("Abortin at user request.")
	local("./manage.py test register")