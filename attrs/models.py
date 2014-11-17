# -*- coding: utf-8 -*-
from django.db import models

from entropy.base import GenericMixin


class Attribute(GenericMixin):
    '''Generic Attribute'''
    name = models.SlugField(max_length=256)
    value = models.CharField(max_length=2048)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s=%s' % (self.name, self.value,)
