# coding: utf-8

from django.shortcuts import render
from handlers.gates import registry


def get_handler(cls_name):
    handler = registry[cls_name]
    return handler()


def index(request):
    return render(request, 'index.html', {})
