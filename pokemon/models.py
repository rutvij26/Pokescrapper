from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class pokemon(models.Model):
        name = models.CharField(max_length=255)
        Types = models.TextField()
        Hp = models.BigIntegerField()
        Attack = models.BigIntegerField()
        Defence = models.BigIntegerField()
        Spattack = models.BigIntegerField()
        Spdefence = models.BigIntegerField()
        Speed = models.BigIntegerField()

