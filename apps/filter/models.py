from django.db import models
# from django.contrib.postgres.fields import JSONField
# Create your models here.
class Filter(models.Model):
    title = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    children= models.JSONField()
    def __str__(self) :
        return str(self.title)