# coding: utf-8

import requests
import datetime
import json

from django.conf import settings

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

    def _build_url(self, *args, **kwargs):
        raise NotImplemented

    def _get_post_data(self, *args, **kwargs):
        raise NotImplemented

    def send(self, *args, **kwargs):
        raise NotImplemented


class CommonHandler(BaseHandler):
    """Common handler class for Smsc and Smstraffic gateway as described in test task"""

    def _parse_response(self, data):
        response = json.loads(data)
        log_entry = LogEntry(
            timestamp=datetime.datetime.now(),
            gatename=self.__class__.__name__,
            status=LogEntry.ERROR if response['status'] == 'error' else LogEntry.OK,
            phone=response.get('phone', ''),
            error_code=response.get('error_code', None),
            error_msg=response.get('error_msg', '')
        )
        log_entry.save()
        return log_entry

    def _build_url(self, data):
        return self.api_url

    def _get_post_data(self, data):
        return {}

    def send(self, data):
        url = self._build_url(data)
        post_data = self._get_post_data(data)

        resp = requests.post(url, params=post_data)
        if not resp.ok:
            log_entry = LogEntry(
                timestamp=datetime.datetime.now(),
                gatename=self.__class__.__name__,
                status=LogEntry.ERROR,
                phone=data.get('phone', ''),
                error_code=resp.status_code,
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


class SmscReal(BaseHandler):
    __metaclass__ = RegisteredClass

    api_url = 'http://smsc.ru/sys/send.php'
    login = settings.SMSC_LOGIN
    password = settings.SMSC_PASSWORD

    def _build_url(self, data):
        qs_dict = dict(
            login=self.login,
            psw=self.password,
            phones=data.get('phone', None),
            mes=data.get('message', None),
            fmt=data.get('fmt', 3),
        )

        qs = ["%s=%s" % (k, v) for k, v in qs_dict.iteritems()]
        return "%s?%s" % (self.api_url, '&'.join(qs))

    def send(self, data):
        url = self._build_url(data)

        resp = requests.post(url)
        if not resp.ok:
            log_entry = LogEntry(
                timestamp=datetime.datetime.now(),
                gatename=self.__class__.__name__,
                status=LogEntry.ERROR,
                phone=data.get('phone', ''),
                error_code=0,
                error_msg=resp.reason
            )
            log_entry.save()
            return log_entry

        log_entry = self._parse_response(resp.content)
        log_entry.phone = data.get('phone', '')
        log_entry.save()
        return log_entry

    def _parse_response(self, data):
        response = json.loads(data)
        log_entry = LogEntry(
            timestamp=datetime.datetime.now(),
            gatename=self.__class__.__name__,
            status=LogEntry.ERROR if 'error' in response else LogEntry.OK,
            phone=response.get('phone', ''),
            error_code=response.get('error_code', None),
            error_msg=response.get('error', '')
        )
        return log_entry
