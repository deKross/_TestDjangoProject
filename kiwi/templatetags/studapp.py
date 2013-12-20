# -*- coding: utf-8 -*-
from django.template import Library, TemplateSyntaxError
from django.template.base import Node, Variable, VariableDoesNotExist
from django.template.loader import render_to_string
from django.db.models import Model
from django.core.urlresolvers import reverse


register = Library()

@register.simple_tag
def admin_link(obj):
    info = obj._meta.app_label, obj._meta.module_name
    return reverse("admin:%s_%s_change" % info, args=(obj.pk,))
