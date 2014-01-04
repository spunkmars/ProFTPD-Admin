#!/usr/local/python27/bin/python

import os,sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'proftpd.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
