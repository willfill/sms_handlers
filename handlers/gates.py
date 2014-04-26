# coding: utf-8

import requests
import datetime
import json

from models import LogEntry

registry = {}


class RegisteredClass(type):
    def __new__(cls, *args, **kwargs):
        newclass = super(RegisteredClass, cls).__new__(cls, *args, **kwargs)
        registry[newclass.__name__] = newclass
        return newclass


class BaseHandler(object):
    def _parse_response(self, response):
        raise NotImplemented

    def _build_url(self, **kwargs):
        raise NotImplemented

    def send(self, *args, **kwargs):
        raise NotImplemented


class CommonHandler(BaseHandler):
    """Common handler class for Smsc and Smstraffic gateway as described in test task"""

    def _parse_response(self, data):
        response = json.loads(data)
        log_entry = LogEntry(
            timestamp=datetime.datetime.now(),
            status=LogEntry.ERROR if response['status'] == 'error' else LogEntry.OK,
            phone=response.get('phone', ''),
            error_code=response.get('error_code', None),
            error_mds=response.get('error_msg', '')
        )
        log_entry.save()
        return log_entry

    def _build_url(self, **kwargs):
        return self.api_url

    def send(self, **kwargs):
        url = self._build_url(kwargs.get('get_args', {}))

        resp = requests.post(url, params=kwargs.get('post_args', {}))
        if not resp.ok:
            log_entry = LogEntry(
                timestamp=datetime.datetime.now(),
                gatename=self.__class__,
                status=LogEntry.ERROR,
                phone=kwargs.get('phones', ''),
                error_code=0,
                error_msg=resp.reason
            )
            log_entry.save()
            return log_entry

        return self._parse_response(resp.content)


class Smsc(CommonHandler):
    __metaclass__ = RegisteredClass

    api_url = 'http://smsc.ru/someapi/message/'


class Smstraffic(CommonHandler):
    __metaclass__ = RegisteredClass

    api_url = 'http://smstraffic.ru/super­api/message/'
