# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.views import generic
from kiwi.models import Student, Group


class GroupsList(generic.ListView):
    model = Group
    context_object_name = "groups"
    template_name = "kiwi/groupslist.html"


class GroupDetails(generic.ListView):
    context_object_name = "students"
    template_name = "kiwi/groupdetails.html"

    def get_queryset(self):
        self.group = get_object_or_404(Group, name=self.args[0])
        return self.group.student_set.order_by("last_name", "first_name").all()

    def get_context_data(self, **kwargs):
        context = super(GroupDetails, self).get_context_data(**kwargs)
        context["group"] = self.group
        return context


class StudentCreate(generic.CreateView):
    model = Student
    template_name = "kiwi/studentcreate.html"

    def get_success_url(self):
        return "/group/%s/" % self.object.group.name

    @method_decorator(permission_required("kiwi.create_student"))
    def dispatch(self, *a, **kw):
        return super(StudentCreate, self).dispatch(*a, **kw)


class StudentUpdate(generic.UpdateView):
    model = Student
    context_object_name = "student"
    template_name = "kiwi/studentupdate.html"

    def get_object(self):
        group = self.args[0]
        lname, fname, patr = self.args[1].split('_')
        return get_object_or_404(Student, group__name=group, first_name=fname,
                                 last_name=lname, patronymic=patr)

    def get_success_url(self):
        return "/group/%s/" % self.object.group.name

    @method_decorator(permission_required("kiwi.change_student"))
    def dispatch(self, *a, **kw):
        return super(StudentUpdate, self).dispatch(*a, **kw)


class StudentDelete(generic.DeleteView):
    model = Student
    context_object_name = "student"
    template_name = "kiwi/studentdelete.html"

    def get_object(self):
        group = self.args[0]
        lname, fname, patr = self.args[1].split('_')
        return get_object_or_404(Student, group__name=group, first_name=fname,
                                 last_name=lname, patronymic=patr)

    def get_success_url(self):
        return "/group/%s/" % self.object.group.name

    @method_decorator(permission_required("kiwi.delete_student"))
    def dispatch(self, *a, **kw):
        return super(StudentDelete, self).dispatch(*a, **kw)
