#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import datetime

from django.db import models



class Report(models.Model):
    """
        Save the result of the custom report form wizard for further
        regeneration. The result is saved as a serialized dictionary.
    """

    class Meta:
        unique_together = (('creation_date', 'name'),)

    name = models.CharField(max_length=64)
    query = models.TextField()
    creation_date = models.DateTimeField(default=datetime.datetime.now,
                                         editable=False)


    def __unicode__(self):
        return self.name
