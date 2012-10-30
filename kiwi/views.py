# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.views import generic
from kiwi import models


class GroupsList(generic.ListView):
    model = models.Group
    # context_object_name = "groups"
    template_name = "groupslist.html"


class GroupDetails(generic.DetailView):
    model = models.Group
    template_name = "groupdetails.html"
