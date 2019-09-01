from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Debater(AbstractUser):
    # username
    # password
    # email
    # first_name
    # last_name
    nickname = models.CharField(max_length=50, blank=True)
    department = models.CharField(max_length=50, blank=True)
    tel = models.CharField(max_length=20, blank=True)
    grade = models.SmallIntegerField(null=True)
    LEVEL_CHOICES = (
        ("FM", "Freshman"),
        ("OF", "Offical"),
        ("RE", "Retired"),
    )
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default="FM") 

    class Meta(AbstractUser.Meta):
        pass

    def init(self, nickname_='', department_='', tel_='', grade_=None, level_="FM"):
        self.nickname = nickname_
        self.department = department_
        self.tel = tel_
        self.grade = grade_
        self.level = level_