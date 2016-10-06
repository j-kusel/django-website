from fabric.api import abort, cd, env, lcd, local, prefix, run, settings
from fabric.contrib.console import confirm
from contextlib import contextmanager as _contextmanager
from os import path
import re

pathname = re.sub('\/fabfile.py$', '', path.realpath(__file__))
projname = re.findall('\/([a-zA-Z]*|\d*)/?$', pathname)[0]
envname = 'site'

env.directory = pathname
env.activate = '. {}/../{}/bin/activate'.format(pathname, envname)
env.colorize_errors = True

apps = [
    'blog',
    'projects',
]
apps.extend(['admin','auth','contenttypes','sessions'])

local_shell = '/bin/bash'

@_contextmanager
def virtualenv():
    with cd(env.directory):
        with prefix(env.activate):
            yield

def test():
    with settings(warn_only=True):
        for a in apps:
            app_test = "./manage.py test {}".format(a)
            result = local(app_test, capture=True)
            if result.failed and not confirm("'{}' tests failed. Continue?".format(a)):
                abort("Aborting at user request.")

def commit():
    local("git add -p && git commit", shell=local_shell)

def push():
    local("git push", shell=local_shell)

def prepare_deployment(branch_name):
    with virtualenv():
        test()
        commit()
        push()

def deploy():
    with virtualenv():
        run('git pull')
        with settings(warn_only=True):                
            for a in apps:
                run('./manage.py migrate {}'.format(a))
        run('./manage.py runserver')
