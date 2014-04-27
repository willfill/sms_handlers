# coding: utf-8

from django.shortcuts import render
from django.template import RequestContext

from handlers.gateways import registry
from handlers.models import LogEntry
from handlers.forms import MessageForm


def get_handler(cls_name):
    handler = registry[cls_name]
    return handler()


def send_page(request):
    error = None
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            try:
                handler = get_handler(form.cleaned_data['gateway'])
                handler.send({
                    'phone': form.cleaned_data['phone'],
                    'message': form.cleaned_data['message']
                })
                form = MessageForm()
            except Exception as e:
                error = 'Improperly configured gateway: %s' % e.message
    else:
        form = MessageForm()

    context = RequestContext(request, {
        'form': form,
        'error': error
    })
    return render(request, 'index.html', context)


def log(request):
    entries = LogEntry.objects.all()
    return render(request, 'log.html', {'entries': entries})
