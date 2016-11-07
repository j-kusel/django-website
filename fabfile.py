from fabric.api import abort, cd, env, lcd, local, prefix, run, settings, sudo
from fabric.contrib import project
from fabric.contrib.console import confirm
from fabric.contrib.files import append, exists, sed
from fabric.decorators import roles
from contextlib import contextmanager as _contextmanager
from os import path
import re, random

REPO_URL = 'https://github.com/ultraturtle0/website.git'
REPO_BRANCH = 'deployment'

PYTHON = 'python3.4'
VIRTUALENV = 'virtualenv'
LOCALVENV = 'site'

APACHE_HOST = '192.168.1.151' # make these dicts with users/env variable psswrds
MYSQL_HOST = '192.168.1.151'
MEDIA_HOST = '192.168.1.151'

APACHE_LOGLEVEL = 'warn'

ADMIN_INFO = {
    'email': 'jordankusel@my.unt.edu',
}

env.roledefs.update({
    'webserver': [APACHE_HOST,],
    'dbserver': [MYSQL_HOST,],
    'mediaserver': [MEDIA_HOST,],
})

pathname = path.dirname(path.realpath(__file__))
projname = re.findall('\/([a-zA-Z]*|\d*)/?$', pathname)[0]

env.directory = pathname
env.proj = projname
env.venv = VIRTUALENV
env.deploy_dir = '/srv/www/{}'.format(env.proj)
env.venv_dir = '{}/{}'.format(env.deploy_dir, env.venv)
env.apache_dir = '/etc/apache2'

env.colorize_errors = True

apps = [
    'blog',
    'projects',
]

local_shell = '/bin/bash'

@_contextmanager
def virtualenv(source):
    with cd(source):
        with prefix('. ../{}/bin/activate'.format(env.venv)):
            yield

def migrate():
    _create_directory_structure_if_necessary()
    env.source_folder = env.deploy_dir + '/source'
    _pull_source(env.source_folder)
    _update_settings(env.source_folder)
    _update_virtualenv(env.source_folder)
    _config_mysql()
    _config_apache()
    _update_database(env.source_folder)

    local_manage = path.dirname(path.realpath(__file__))
    _migrate_static(env.source_folder)
    #_run_server(source_folder)

def update():
    env.source_folder = env.deploy_dir + '/source'
    _fetch_git(env.source_folder)
    _update_database(env.source_folder)
    _migrate_static(env.source_folder)

@roles('webserver')
def _fetch_git(source):
    if exists(source + '/.git'):
        sudo('cd {} && git fetch'.format(source))

@roles('webserver')
def _create_directory_structure_if_necessary():
    sudo('mkdir -p {}'.format(env.deploy_dir))
    for subfolder in ('static', 'media', env.venv, 'source'):
        sudo('mkdir -p {}/{}'.format(env.deploy_dir, subfolder))

@roles('webserver')
def _pull_source(source):
    sudo('git clone {} --branch {} --single-branch {}'.format(REPO_URL, REPO_BRANCH, source))

    # CHECK LOCAL COMMIT
    # current_commit = local('git log -n 1 --format=%H', capture=True)
    # HARD RESET SERVER CODE
    # run('cd {} && git reset --hard {}'.format(source, current_commit))

@roles('webserver')
def _update_settings(source):
    settings_path = '{}/{}/settings.py'.format(source, env.proj)
    sudo('mv {}/{}/settings_deploy.py {}'.format(source, env.proj, settings_path))

    # TURN OFF DEBUG MODE
    sed(settings_path, "DEBUG.*$", "DEBUG = False", use_sudo=True)

    # CHANGE ALLOWED HOSTS
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["%s"]' % (env.host),
        use_sudo=True
    )

    # CHANGE STATIC_ROOT / MEDIA_ROOT PATHS
    run(r"sudo sed -i.bak -r -e 's/STATIC_ROOT =.*$/STATIC_ROOT = os.path.join(BASE_DIR, '\''..\/static'\'')/g' {}".format(settings_path))
    append(settings_path, "MEDIA_URL = '/media/'", use_sudo=True)
    append(settings_path, "MEDIA_ROOT = os.path.join(BASE_DIR, '../media')", use_sudo=True)

    # INSTALL mod_wsgi.server
    run(r"sudo sed -i.bak -r -e 's/INSTALLED_APPS.*$/INSTALLED_APPS = ['\''mod_wsgi.server'\'',/g' {}".format(settings_path))

    # CHANGE DATABASES
    sudo(r"sed -i.bak -r -e 's/DATABASES = \{/DATABASES = \{'\''default'\'': \{'\''ENGINE'\'': '\''django.db.backends.mysql'\'', '\''NAME'\'': '\''%s_db'\'', '\''USER'\'': '\''root'\'', '\''PASSWORD'\'': '\''raspberry'\'', '\''HOST'\'': '\''%s'\'', '\''PORT'\'':'\'''\'',\},/g' %s" % (env.proj, MYSQL_HOST, settings_path))

    # GENERATE A NEW KEY (keep key constant after initial deploy)
    secret_key_file = '{}/{}/secret_key.py'.format(source, env.proj)
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '{}'".format(key), use_sudo=True)
    append(settings_path, 'from .secret_key import SECRET_KEY', use_sudo=True)

@roles('webserver')
def _update_virtualenv(source):
    if not exists(env.venv_dir + '/bin/pip'):
        sudo('pip install -U pip')
        sudo('pip install virtualenv')
        sudo('virtualenv -p {} {}'.format(PYTHON, env.venv_dir))
    # CHANGE VIRTUALENV OWNERSHIP
    sudo('chown -R {0}:{0} {1}/'.format(env.user, env.venv_dir))

    run('{}/bin/pip install -r {}/requirements.txt'.format(env.venv_dir, source))

@roles('dbserver')
def _config_mysql():
    # BIND ADDRESS TO WEBSERVER

    # UPDATE PACKAGES, INSTALL MYSQL
    sudo('apt-get -y update && sudo apt-get -y upgrade')
    sudo('apt-get install -y mysql-server && apt-get install -y mysql-client')

    # BUILD DATABASE, CHANGE PERMISSIONS
    sudo('echo "CREATE DATABASE {}_db;" | mysql --user=root --password=raspberry'.format(env.proj))
    sudo("""echo "GRANT ALL ON {}_db.* TO root@{} IDENTIFIED BY 'raspberry';" | mysql --user=root --password=raspberry""".format(env.proj, APACHE_HOST))

    # CHANGE BIND-ADDRESS
    mysql_conf_path = '/etc/mysql/my.cnf'
    sed(mysql_conf_path, 
        'bind-address.*$',
        'bind-address = {}'.format(APACHE_HOST),
        use_sudo=True)

    # RESTART MYSQL
    sudo('service mysql restart')

@roles('webserver')
def _config_apache():
    # INSTALL APACHE PACKAGES
    sudo('apt-get -y update')
    sudo('apt-get -y install python3-pip')
    sudo('apt-get -y install apache2')
    sudo('apt-get -y install libapache2-mod-wsgi-py3')

    # ENABLE MOD_WSGI
    sudo('a2enmod wsgi')

    #sudo("echo '<Directory {}/source>\n\t<Files wsgi.py>\n\tRequire all granted\n\t</Directory>' >> {}/apache2.conf".format(env.deploy_dir, env.apache_dir))

    # MOVE / EDIT CONFIG TEMPLATE FILE (apache.conf)
    apache_config_path = '{}/sites-available/{}.conf'.format(env.apache_dir, env.proj)
    sudo('mv {}/source/apache.conf {}'.format(env.deploy_dir, apache_config_path))

    APACHE_DICT = {
        'SERVERADMIN': ADMIN_INFO['email'],
        'SERVERNAME': env.proj,
        'SERVERALIAS': env.host_string,
        'SERVERROOT': env.deploy_dir,
        'VIRTUALENV': '{}/{}'.format(env.deploy_dir, env.venv),
        'PYTHON': PYTHON,
        'STATICROOT': env.deploy_dir,
        'MEDIAROOT': env.deploy_dir,
        'LOGLEVEL': APACHE_LOGLEVEL,
    }

    for s in APACHE_DICT:
        sed(apache_config_path, s, APACHE_DICT[s], use_sudo=True)

    # ENABLE SITE
    sudo('a2ensite {}'.format(env.proj))

    # CHANGE OWNERSHIP TO APACHE
    sudo('chown -R www-data:www-data {}'.format(env.deploy_dir))
    sudo('apache2ctl restart')

@roles('webserver')
def _update_database(source):
    with virtualenv(source):
        run('python3 manage.py makemigrations --noinput')
        run('python3 manage.py migrate --noinput')

def deploy():
    with virtualenv():
        run('git pull')
        with settings(warn_only=True):                
            for a in (apps + ['admin','auth','contenttypes','sessions']):
                run('./manage.py migrate {}'.format(a))
    run_server()

@roles('mediaserver')
def _migrate_static(source):
    # INSTALL RSYNC ON LOCAL AND MEDIA MACHINES
    # local('sudo apt-get -y install rsync')
    # sudo('apt-get -y install rsync')

    # COLLECTSTATIC AND SYNC MEDIA
    # static_new = env.deploy_dir + '/../static/'
    # static = path.join(source, 'static/')
    with cd(source):
        sudo('{}/bin/python3 manage.py collectstatic --noinput'.format(env.venv_dir))
    # project.rsync_project(remote_dir=static_new, local_dir=static)
