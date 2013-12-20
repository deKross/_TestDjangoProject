# encoding: utf-8

import time
from django.utils.encoding import smart_unicode
from django.db.backends import BaseDatabaseWrapper

old_cursor = BaseDatabaseWrapper.cursor

def cursor(self):
    StatsMiddleware.sql_count += 1
    return old_cursor(self)

BaseDatabaseWrapper.cursor = cursor

class StatsMiddleware(object):
    sql_count = 0

    def process_request(self, request):
        StatsMiddleware.sql_count = 0
        self._time = time.time()

    def process_response(self, request, response):
        total = (time.time() - self._time) * 1000
        total = "%0.2fms | %d" % (total, StatsMiddleware.sql_count)
        response.content = smart_unicode(response.content).replace(u'</body>', u"%s</body>" % total)
        return response
