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


class SimpleAttrMixin(models.Model):
    '''
    INCOMPLETE.


    class Widget(models.Model):

    class WidgetAttr(SimpleAttrMixin):
        widget = models.ForeignKey(Widget)
        # name
        # value


    Adds `name`, `value` pair to an object and gives the ability to 
    reference those values through a dict style lookup, or via
    dot notation in templates.

    For example:

    class Widget(SimpleAttrMixin):
        widget = models.ForeignKey('Widget')

    # ...

    widget_attr = WidgetAttr(
        widget = widget,
        name = 'foo',
        value = 'bar')

    widget_attr.save()
    print widget_attr.foo
    >>> 'bar'
    widget_attr.foo = 'boo'
    widget_attr.save()
    print widget_attr.foo
    >>> 'boo'

    widget.foo
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
