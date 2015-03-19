from django.db import models
from django.contrib.auth.models import User, Group
import datetime

class Category(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    short_name = models.CharField(max_length=5, blank=True, null=True)
    description = models. TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return unicode(self.name)

class Entry(models.Model):
    date = models.DateField(auto_now=True)
    username = models.ForeignKey(User, default=1)
    modified = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    description = models.CharField(max_length=40, blank=True, null=True)
    category = models.ForeignKey(Category)
    hours = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)


