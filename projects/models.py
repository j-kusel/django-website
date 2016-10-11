from django.db import models

# Create your models here.

class Type(models.Model):
    title = models.CharField(max_length=30, blank=False, null=True)

    def __unicode__(self):
        return self.title
 
class Project(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    media = models.URLField(max_length=200, blank=True, null=True)
    score = models.URLField(max_length=200, blank=True, null=True)
    category = models.ForeignKey('Type', on_delete=models.CASCADE)

    def __unicode__(self):
        return u'{} ({})'.format(self.title, self.category)
