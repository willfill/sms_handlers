# coding: utf-8

from django.http import HttpResponse
from handlers.gates import registry


def get_handler(cls_name):
    handler = registry[cls_name]
    return handler()


def stub(request):
    return HttpResponse('OK')
