from __future__ import unicode_literals

from django.db import models

class record(models.Model):
    kind = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    detail = models.CharField(max_length=200)
    who = models.CharField(max_length=300)
    when = models.DateField()
    soc = models.IntegerField(default=0)
    def __str__(self):
        return (self.name + ' ' + self.who + ' ' + str(self.when))#.encode('utf-8')
# Create your models here.
