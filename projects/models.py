from django.db import models

# Create your models here.

class Type(models.Model):
    title = models.CharField(default='misc', max_length=30, blank=False, null=True)

    def __str__(self):
        return self.title
 
class Project(models.Model):
    title = models.CharField(default='demo', max_length=100, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)

    img = models.FileField(upload_to='images', blank=True, null=True)
    score = models.FileField(upload_to='scores', blank=True, null=True)
    #audio = models.URLField(max_length=200, blank=True, null=True)

    category = models.ForeignKey('Type', on_delete=models.CASCADE)

    def __str__(self):
        return '{} ({})'.format(self.title, self.category)
