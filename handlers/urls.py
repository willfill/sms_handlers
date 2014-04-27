# coding: utf-8

from django.conf.urls import patterns, url
import views as v

urlpatterns = patterns('',
    url(r'^$', v.index, name='index'),
    url(r'^logs/$', v.log, name='log')
)
