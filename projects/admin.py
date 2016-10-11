from django.contrib import admin

# Register your models here.
from .models import Project, Type

class ProjectAdmin(admin.ModelAdmin):
    class Meta:
        model = Project

class TypeAdmin(admin.ModelAdmin):
    class Meta:
        model = Type

admin.site.register(Project, ProjectAdmin)
admin.site.register(Type, TypeAdmin)
