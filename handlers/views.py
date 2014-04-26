# coding: utf-8

from django.http import HttpResponse
import sms_gates


def get_handler(cls_name):
    handler = getattr(sms_gates, cls_name)
    return handler()


def stub(request):
    return HttpResponse('OK')
