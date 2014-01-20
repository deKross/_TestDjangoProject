# encoding: utf-8

import time
from threading import currentThread

from django.utils.encoding import smart_unicode
from django.db.backends import BaseDatabaseWrapper


old_cursor = BaseDatabaseWrapper.cursor

def cursor(self):
    data = StatsMiddleware.get_data()
    if data is not None:
        data.sql_count += 1
    return old_cursor(self)

BaseDatabaseWrapper.cursor = cursor


class StatsData(object):
    __slots__ = ['begin_time', 'sql_count']

    def __init__(self):
        self.begin_time = time.time()
        self.sql_count = 0

    @property
    def total_time(self):
        return (time.time() - self.begin_time) * 1000


class StatsMiddleware(object):
    data = {}

    @classmethod
    def get_data(cls):
        return cls.data.get(currentThread().ident)

    def process_request(self, request):
        self.__class__.data[currentThread().ident] = StatsData()

    def process_response(self, request, response):
        data = self.get_data()
        if (not data or request.is_ajax() or
                ('gzip' in response.get('Content-Encoding', '')) or
                (response.get('Content-Type', '').split(';')[0] != 'text/html')):
            return response
        total = "%0.2fms | %d" % (data.total_time, data.sql_count)
        del self.__class__.data[currentThread().ident]
        response.content = smart_unicode(response.content).replace(
                u'</body>', u"%s</body>" % total)
        return response
