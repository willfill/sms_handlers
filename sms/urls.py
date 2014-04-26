# coding: utf-8

from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', include('handlers.urls')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
