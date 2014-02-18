# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import namedtuple

from django.http import Http404, HttpResponseRedirect
from django.db.models import Count
from django.contrib.auth import get_permission_codename
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.views import generic
from django.views.generic.edit import (BaseCreateView, BaseUpdateView,
                                       BaseDeleteView)

from studapp.models import Student, Group, LogEntry, ADDITION, DELETION


class Log(generic.ListView):
    AdditionData = namedtuple('AdditionData', 'field value')
    ChangeData = namedtuple('ChangeData', 'field old new')
    ActionFlag = namedtuple('ActionFlag', 'addition change deletion')

    model = LogEntry
    context_object_name = 'entries'
    template_name = 'studapp/log.html'

    def get_queryset(self):
        qs = super(Log, self).get_queryset()
        for item in qs:
            item.commiter = '[system]' if item.user is None else item.user
            f = [False] * 3
            f[item.action_flag] = True
            item.action = Log.ActionFlag(*f)
            if item.action_flag == DELETION or not item.data:
                continue
            elif item.action_flag == ADDITION:
                dataclass = Log.AdditionData
                delta = 2
            else:
                dataclass = Log.ChangeData
                delta = 3
            data = item.data.split('%%')
            fields = item.content_type.model_class()._meta.fields
            data = [dataclass(fields[int(data[idx])].verbose_name,
                              *data[idx+1:idx+delta])
                    for idx in xrange(0, len(data), delta)]
            item.data = data
        return qs

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return super(Log, self).dispatch(request, *args, **kwargs)


class GroupsList(generic.ListView):
    model = Group
    context_object_name = 'groups'
    template_name = 'studapp/groupslist.html'

    def get_queryset(self):
        return self.model.objects \
                         .order_by('name') \
                         .select_related('praepostor') \
                         .annotate(students_count=Count('student'))


class GroupDetails(generic.ListView):
    context_object_name = 'students'
    template_name = 'studapp/groupdetails.html'

    def get_queryset(self):
        students = Student.objects \
                          .filter(group__name=self.kwargs['group']) \
                          .select_related('group__praepostor') \
                          .order_by('last_name', 'first_name')
        if not students:
            raise Http404('No Group matches the given query.')
        return students

    def get_context_data(self, **kwargs):
        context = super(GroupDetails, self).get_context_data(**kwargs)
        group = self.object_list[0].group
        context['group'] = group
        context['praepostor'] = group.praepostor
        return context


class EditMixin(object):
    fields = '__all__'

    def _get_type(self):
        if isinstance(self, BaseCreateView):
            return 'add'
        elif isinstance(self, BaseUpdateView):
            return 'change'
        elif isinstance(self, BaseDeleteView):
            return 'delete'
        raise ImproperlyConfigured(
                "%s should inherit from "
                "Base<Create|Update|Delete>View." % self.__class__.__name__)

    def _get_permission(self):
        if hasattr(self, '_permission'):
            return self._permission

        self._permission = (self.model._meta.app_label,
                            get_permission_codename(self._get_type(),
                                                    self.model._meta))
        return self._permission

    def get_action_url(self):
        return getattr(self, 'action_url', '')

    def get_submit_label(self):
        return getattr(self, 'submit_label', '')

    def get_context_data(self, **kwargs):
        context = {}
        context['action_url'] = self.get_action_url()
        context['submit_label'] = self.get_submit_label()
        context.update(kwargs)
        return super(EditMixin, self).get_context_data(**context)

    def get_template_names(self):
        try:
            names = super(EditMixin, self).get_template_names()
        except ImproperlyConfigured:
            names = []

        name = '/'.join(self._get_permission())
        name = "%s.html" % name

        names.append(name)
        return names

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object._commiter = self.request.user
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object._commiter = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('.'.join(self._get_permission())):
            return super(EditMixin, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class StudentEditMixin(EditMixin):
    model = Student
    template_name = 'studapp/edit.html'
    context_object_name = "student"

    def get_action_url(self):
        return reverse(self._get_permission()[1], kwargs={
            'group': self.object.group.name,
            'first_name': self.object.first_name,
            'last_name': self.object.last_name,
            'patronymic': self.object.patronymic})

    def get_object(self):
        return get_object_or_404(Student, group__name=self.kwargs['group'],
                                 first_name=self.kwargs['first_name'],
                                 last_name=self.kwargs['last_name'],
                                 patronymic=self.kwargs['patronymic'])

    def get_success_url(self):
        return reverse('group', kwargs={'group': self.object.group.name})


class GroupEditMixin(EditMixin):
    model = Group
    template_name = 'studapp/edit.html'
    context_object_name = 'group'

    def get_action_url(self):
        return reverse(self._get_permission()[1],
                       kwargs={'group': self.object.name})

    def get_object(self):
        return get_object_or_404(Group, name=self.kwargs['group'])

    def get_success_url(self):
        return reverse('group', kwargs={'group': self.object.name})


class StoreOldFieldsValuesMixin(object):
    def get_object(self):
        obj = super(StoreOldFieldsValuesMixin, self).get_object()
        self.old_fields = [f.value_from_object(obj) for f in obj._meta.fields]
        return obj

    def form_valid(self, form):
        self.object._old_fields = self.old_fields
        return super(StoreOldFieldsValuesMixin, self).form_valid(form)


class StudentCreate(StudentEditMixin, generic.CreateView):
    submit_label = 'Добавить'

    def get_action_url(self):
        return reverse('add_student')


class StudentUpdate(StoreOldFieldsValuesMixin,
                    StudentEditMixin, generic.UpdateView):
    submit_label = 'Сохранить'


class StudentDelete(StudentEditMixin, generic.DeleteView):
    submit_label = 'Удалить'


class GroupCreate(GroupEditMixin, generic.CreateView):
    submit_label = 'Добавить'

    def get_action_url(self):
        return reverse('add_group')


class GroupUpdate(StoreOldFieldsValuesMixin,
                  GroupEditMixin, generic.UpdateView):
    submit_label = 'Сохранить'


class GroupDelete(GroupEditMixin, generic.DeleteView):
    submit_label = 'Удалить'
