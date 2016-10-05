from fabric.api import abort, cd, env, lcd, local, prefix, run, settings
from fabric.contrib.console import confirm
from contextlib import contextmanager as _contextmanager

projname = 'kusel'
dirname = 'website'
envname = 'site'

env.directory = '/home/pi/python/{}'.format(dirname)
env.activate = 'source /home/pi/python/{}/{}/bin/activate'.format(dirname, envname)
env.colorize_errors = True

apps = [
    'blog',
]

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
        with lcd(projname):
            test()
            commit()
            push()

def deploy():
    with virtualenv():
        with lcd(projname):
            run('git pull')
            for a in apps:
                run('./manage.py migrate {}'.format(a))
            run('./manage.py runserver')
