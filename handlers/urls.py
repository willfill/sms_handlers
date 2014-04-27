# coding: utf-8

from django.conf.urls import patterns, url
import handlers.views as v

urlpatterns = patterns('',
    url(r'^$', v.send_page, name='send_page'),
    url(r'^logs/$', v.log, name='log')
)
