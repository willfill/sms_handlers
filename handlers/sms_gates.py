# coding: utf-8

from abc import ABCMeta, abstractmethod
import requests


class BaseHandler:
    __metaclass__ = ABCMeta

    @abstractmethod
    def send(self, params):
        raise NotImplemented


class Smsc(BaseHandler):
    url = 'http://smsc.ru/some­api/message/'

    def send(self, phone, msg):
        payload = {
            'phone': phone,
            'msg': msg
        }
        resp = requests.post(self.url, params=payload)
        if not resp.ok:
            return {
                'status': 'error',
                'phone': phone,
                'error_code': 0,
                'error_msg': resp.reason
            }
        return resp.json()
