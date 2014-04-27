# coding: utf-8

import requests
import datetime
import json
from abc import ABCMeta, abstractmethod

from django.conf import settings

from handlers.models import LogEntry


registry = {}


def register(cls):
    registry[cls.__name__] = cls
    return cls


class BaseHandler(object):
    """Defines sms handler interface"""

    __metaclass__ = ABCMeta

    @abstractmethod
    def _parse_response(self, response):
        raise NotImplemented

    @abstractmethod
    def _build_url(self, *args, **kwargs):
        raise NotImplemented

    @abstractmethod
    def _get_post_data(self, *args, **kwargs):
        raise NotImplemented

    @abstractmethod
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


@register
class Smsc(CommonHandler):
    api_url = 'http://smsc.ru/someapi/message/'


@register
class Smstraffic(CommonHandler):
    api_url = 'http://smstraffic.ru/super­api/message/'


@register
class SmscReal(BaseHandler):
    """Siple handler for real smsc.ru gateway"""

    api_url = 'http://smsc.ru/sys/send.php'

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
        # не сохраняем log_entry, так как нам нужно добавить иформацию о номере (реальный гейт ее не возвращает)
        return log_entry

    def _get_post_data(self, data):
        return {}

    def _build_url(self, data):
        qs_dict = dict(
            login=settings.SMSC_LOGIN,
            psw=settings.SMSC_PASSWORD,
            phones=data.get('phone', None),
            mes=data.get('message', None),
            fmt=data.get('fmt', 3),  # гейт будет возвращать ответ в json
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
