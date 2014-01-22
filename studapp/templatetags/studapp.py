# -*- coding: utf-8 -*-
from functools import wraps

from django.template import Library
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.core.urlresolvers import reverse


register = Library()


def exception_wrapper(func):
    @wraps(func)
    def wrap(*a, **kw):
        try:
            return func(*a, **kw)
        except Exception as e:
            if settings.TEMPLATE_DEBUG:
                raise e
            return ''

    return wrap


@register.simple_tag
@exception_wrapper
def admin_link(obj):
    info = obj._meta.app_label, obj._meta.model_name
    return reverse("admin:%s_%s_change" % info, args=(obj.pk,))


@register.filter
@exception_wrapper
@stringfilter
def getel(value, arg):
    return value.split('|')[int(arg)].strip()
