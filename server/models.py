# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
# Create your models here.

class MLModel(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField()
    accuracy = models.DecimalField(max_digits=5, decimal_places=3)
    file = models.FileField(upload_to='models/',default='dummy.txt')
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    user=models.CharField(max_length=120,default="Annonymous")
    active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("stars:create", kwargs={"id":self.id})
