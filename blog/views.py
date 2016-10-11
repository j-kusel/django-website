from django.shortcuts import render

# Create your views here.

def sound_page(request):
    return render(request, 'blog/sound.html')
