from django.shortcuts import render
from .models import Project, Type

# Create your views here.

def proj_page(request, type=''):
    category = Type.objects.filter(title=type)
    if category:
        projs = Project.objects.filter(category=Type.objects.get(title=type))
        types = Type.objects.all()
        return render(request, 'projects/{}.html'.format(type), {'projs': projs, 'types': types})
    else:
        return render(request, 'projects/sound.html', {'projs': []})
