# -*- coding: utf-8 -*-
from cms.exceptions import ToolbarAlreadyRegistered
from cms.utils.conf import get_cms_setting
from cms.utils.django_load import load, iterload_objects
from django.core.exceptions import ImproperlyConfigured


class ToolbarPool(object):
    def __init__(self):
        self.toolbars = {}
        self.reverse = {}
        self.discovered = False
        self.block_register = False

    def discover_toolbars(self):
        if self.discovered:
            return
            #import all the modules
        toolbars = get_cms_setting('TOOLBARS')
        if toolbars:
            self.block_register = True
            for cls in iterload_objects(toolbars):
                self.block_register = False
                self.register(cls)
                self.block_register = True
            self.block_register = False
        else:
            load('cms_toolbar')
        self.discovered = True

    def clear(self):
        self.apps = {}
        self.discovered = False

    def register(self, callback):
        if self.block_register:
            return
        # validate the app
        if not callable(callback):
            raise ImproperlyConfigured("Toolbar callbacks must be callable, %r isn't." % callback)
        name = "%s.%s" % (callback.__module__, callback.__name__)
        if name in self.toolbars.keys():
            raise ToolbarAlreadyRegistered("[%s] a toolbar with this name is already registered" % name)
        self.toolbars[name] = callback
        self.reverse[callback] = name
        return callback # return so it can be used as a decorator

    def get_app_key(self, callback):
        return self.reverse[callback]

    def get_toolbars(self):
        self.discover_toolbars()
        return self.toolbars

toolbar_pool = ToolbarPool()
