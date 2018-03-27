from django.shortcuts import render
from .models import Project, Type

# Create your views here.

def proj_page(request, type='', cat=''):
    category = Type.objects.filter(title=type)
    types = Type.objects.filter(category=cat)
    if category:
        projs = Project.objects.filter(category=Type.objects.get(title=type)).order_by('-year')
        print(projs)
        return render(request, 'projects/portfolio.html', {'projs': projs, 'types': types, 'cat': cat})
    else:
        return render(request, 'projects/portfolio.html', {'projs': [], 'types': types, 'cat': cat})

