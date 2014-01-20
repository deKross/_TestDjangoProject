# -*- coding: utf-8 -*-
from django.template import Library
from django.core.urlresolvers import reverse


register = Library()

@register.simple_tag
def admin_link(obj):
    info = obj._meta.app_label, obj._meta.model_name
    return reverse("admin:%s_%s_change" % info, args=(obj.pk,))
