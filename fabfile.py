from fabric.api import abort, cd, env, lcd, local, prefix, run, settings
from fabric.contrib import project
from fabric.contrib.console import confirm
from fabric.contrib.files import append, exists, sed
from contextlib import contextmanager as _contextmanager
from os import path
import re, random

REPO_URL = 'https://github.com/ultraturtle0/website.git'

pathname = re.sub('\/fabfile.py$', '', path.realpath(__file__))
projname = re.findall('\/([a-zA-Z]*|\d*)/?$', pathname)[0]
envname = 'site'

env.directory = pathname
env.proj = projname
env.activate = '. {}/../{}/bin/activate'.format(pathname, envname)
env.colorize_errors = True

apps = [
    'blog',
    'projects',
]

local_shell = '/bin/bash'

@_contextmanager
def virtualenv():
    with cd(env.directory):
        with prefix(env.activate):
            yield

def e(name='production'):
    env.update(environments[name])
    env.environment = name

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

def run_server(host='127.0.0.1', port='8000'):
    with virtualenv():
        run('./manage.py runserver {}:{}'.format(host, port))

def migrate():
    site_folder = '/home/{}/django/{}'.format(env.user, env.host)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(env.directory)
    _pull_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_database(source_folder)
    _run_server(source_folder)


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run('mkdir -p {}/{}'.format(site_folder, subfolder))

def _pull_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd {} && git fetch'.format(source_folder))
    else:
        run('git clone {} {}'.format(REPO_URL, source_folder))
    # CHECK LOCAL COMMIT
    current_commit = local('git log -n 1 --format=%H', capture=True)
    # HARD RESET SERVER CODE
    run('cd {} && git reset --hard {}'.format(source_folder, current_commit))

def _update_settings(source_folder, site_name):
    settings_path = '{}/{}/settings.py'.format(source_folder, env.proj)
    # TURN OFF DEBUG
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    # CHANGE ALLOWED HOSTS
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["%s"]' % (site_name,)
    )
    secret_key_file = '{}/{}/secret_key.py'.format(source_folder, env.proj)
    # GENERATE A NEW KEY (keep key constant after initial deploy)
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '{}'".format(key))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv -p python3.4 ' + virtualenv_folder)
    run('{}/bin/pip install -r {}/requirements.txt'.format(virtualenv_folder, source_folder))

def _run_server(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py runserver 0:8000' % (source_folder,))

def _update_database(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput' % (source_folder,))

def deploy():
    with virtualenv():
        run('git pull')
        with settings(warn_only=True):                
            for a in (apps + ['admin','auth','contenttypes','sessions']):
                run('./manage.py migrate {}'.format(a))
    run_server()

def static_server(remote='staticfiles/'):
    env.hosts = ['192.168.1.150',]
    source_folder = path.dirname(path.abspath(__file__))
    static_folder = path.join(source_folder, 'static/')
    with lcd(source_folder):
        with prefix('. ../virtualenv/bin/activate'):
            local('python3 manage.py collectstatic')
            project.rsync_project(remote_dir=remote, local_dir=static_folder)
