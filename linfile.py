from linen.util import checkpass

# the location of your remote repository + branch
REPO_URL = 'https://github.com/ultraturtle0/website.git'
REPO_BRANCH = 'master'

# version of Python3 in use
PYTHON = 'python3.4'

# desired name of the deployment virtual environment(s)
VIRTUALENV = 'virtualenv'

# desired name of Django project folder
PROJECT_DIR = 'kusel'

# directory name of the local virtual environment -
# it should share a parent directory with the root folder
# of your Django development site
LOCALENV = 'site'

# host IPs (NOTE: currently only supports one at a time)
APACHE_HOSTS = '138.197.20.29'
MYSQL_HOSTS = '138.197.20.29'
MEDIA_HOSTS = '138.197.20.29'

# domain names for Apache that Django will ALLOW
# if DOMAIN_NAMES is a list, the first item will be assigned as ServerName
# and the others will be under ServerAlias
DOMAIN_NAMES = 'jordankusel.xyz'

# verbosity of /var/log/apache2/error.log file
# options from brief to verbose are:
# 'emerg', 'alert', 'crit', 'error', 'warn', 'notice', 'info', 'debug'
APACHE_LOGLEVEL = 'warn'

LINUX_USER = 'jordankusel'

# store PASSWORDS as a dictionary in a passwords.py file in the
# Django root directory, then remove this from your version control!
# do NOT override PASSWORDS below!
PASSWORDS = checkpass()

# register Django superuser + MySQL/Apache info
SUPERUSER = {
    'name': 'Jordan Kusel',
    'username': 'jordankusel',
    'email': 'jordankusel@my.unt.edu',
    'password': '',
}

GIT_INFO = {
    'username': 'jordankusel',
    'email': 'jordankusel@my.unt.edu',
}

MYSQL_INFO = {
    'user': '',
}

APACHE_INFO = {
    'user': '',
    'name': SUPERUSER['name'],
    'email': SUPERUSER['email'],
}
