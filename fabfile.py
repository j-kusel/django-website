from fabric.api import abort, cd, lcd, local, run, settings
from fabric.contrib.console import confirm

def test():
    with settings(warn_only=True):
        result = local("./manage.py test blog", capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")

def commit():
    local("git add -p && git commit")

def push():
    local("git push")

def prepare_deployment(branch_name):
    test()
    commit()
    push()

def deploy():
    code_dir = '/home/pi/python/website/kusel/'
    with cd(code_dir):
        run('git pull')
        run('python manage.py migrate blog')
        run('python manage.py runserver')
