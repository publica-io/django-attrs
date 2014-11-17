# -*- coding: utf-8 -*-
from django.contrib.contenttypes import generic
from django.db import models

from .models import Attribute


class GenericAttrMixin(models.Model):
    '''
    Mixin to give dict access to generic Attributes
    '''

    attributes = generic.GenericRelation('attrs.Attribute')

    class Meta:
        abstract = True

    def _attributes(self):
        return dict(self.attributes.values_list('name', 'value'))

    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except AttributeError:
            return self._attributes()[key]

    def __setitem__(self, key, value):
        from .models import Attribute
        try:
            attr = self.attributes.get(name=key)
        except Attribute.DoesNotExist:
            attr = Attribute(name=key, content_object=self)
        attr.value = value
        attr.save()

        del self._attributes


class SimpleAttrMixin(models.Model):
    '''
    Adds `name`, `value` pair to an object and gives the ability to 
    reference those values through a dict style lookup, or via
    dot notation in templates.

    For example:

    class Widget(SimpleAttrMixin):
        widget = models.ForeignKey('Widget')

    # ...

    widget_field = WidgetField(
        widget = widget,
        name = 'foo',
        value = 'bar')

    widget_field.save()
    print widget_field.foo
    >>> 'bar'
    widget_field.foo = 'boo'
    widget_field.save()
    print widget_field.foo
    >>> 'boo'

    '''
    
    name = models.SlugField(max_length=256)
    value = models.CharField(max_length=2048)

    class Meta:
        abstract = True

    def _attributes(self):
        return dict({self.name: self.value})

    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except AttributeError:
            return self._attributes()[key]

    def __setitem__(self, key, value):
        
        if self.name == key:
            self.value = value
            self.save()
