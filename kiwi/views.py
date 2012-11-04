# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.views import generic
from .models import Student, Group


class GroupsList(generic.ListView):
    model = Group
    context_object_name = "groups"
    template_name = "groupslist.html"


class GroupDetails(generic.ListView):
    context_object_name = "students"
    template_name = "groupdetails.html"

    def get_queryset(self):
        self.group = get_object_or_404(Group, name=self.args[0])
        return self.group.student_set.all()

    def get_context_data(self, **kwargs):
        context = super(GroupDetails, self).get_context_data(**kwargs)
        context["group"] = self.group
        return context
