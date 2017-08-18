# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..login_app.models import User

# Create your models here.

class ActivityManager(models.Manager):

    # Creates a new activity.
    def newAct(self, activity, user):
        activity = self.create(content = activity,
                    user = user
        )
        return activity

class Activity(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name = "activities")
    created_at = models.DateTimeField(auto_now_add = True)
    objects = ActivityManager()