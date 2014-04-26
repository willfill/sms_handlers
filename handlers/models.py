# coding: utf-8

from django.db import models


class LogEntry(models.Model):
    OK = 'OK'
    ERROR = 'ERROR'
    STATUS_CHOICES = (
        (OK, 'ok'),
        (ERROR, 'error')
    )

    timestamp = models.DateTimeField()
    gatename = models.CharField(max_length=30)
    phone = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    error_code = models.IntegerField(null=True)
    error_msg = models.TextField(null=True)
