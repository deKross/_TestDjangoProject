# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.views import generic
from django.views.generic.edit import BaseCreateView, BaseUpdateView, BaseDeleteView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from kiwi.models import Student, Group


class GroupsList(generic.ListView):
    model = Group
    context_object_name = "groups"
    template_name = "kiwi/groupslist.html"


class GroupDetails(generic.ListView):
    context_object_name = "students"
    template_name = "kiwi/groupdetails.html"

    def get_queryset(self):
        self.group = get_object_or_404(Group, name=self.kwargs['group'])
        return self.group.student_set.order_by("last_name", "first_name").all()

    def get_context_data(self, **kwargs):
        context = super(GroupDetails, self).get_context_data(**kwargs)
        context["group"] = self.group
        return context


class EditMixin(object):
    def _get_type(self):
        if isinstance(self, BaseCreateView):
            return 'add'
        elif isinstance(self, BaseUpdateView):
            return 'change'
        elif isinstance(self, BaseDeleteView):
            return 'delete'
        # TODO: Must raise some exception

    def _get_permission(self):
        if hasattr(self, '_permission'):
            return self._permission

        method = "get_%s_permission" % self._get_type()
        method = getattr(self.model._meta, method)

        self._permission = (self.model._meta.app_label, method())
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

    def form_valid(self, form):
        self.object._commiter = self.request.user
        return super(EditMixin, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('.'.join(self._get_permission())):
            return super(EditMixin, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class StudentEditMixin(EditMixin):
    model = Student
    template_name = 'kiwi/edit.html'
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
    template_name = 'kiwi/edit.html'
    context_object_name = 'group'

    def get_action_url(self):
        return reverse(self._get_permission()[1], kwargs={'group': self.object.name})

    def get_object(self):
        return get_object_or_404(Group, name=self.kwargs['group'])

    def get_success_url(self):
        return reverse('group', kwargs={'group': self.object.name})


class StoreOldFieldsValuesMixin(object):
    def form_valid(self, form):
        fields = self.object._meta.fields
        self.object._old_fields = (f.value_from_object(self.object) for f in fields)
        return super(StoreOldFieldsValuesMixin, self).form_valid(form)


class StudentCreate(StudentEditMixin, generic.CreateView):
    submit_label = 'Добавить'

    def get_action_url(self):
        return reverse('add_student')


class StudentUpdate(StoreOldFieldsValuesMixin, StudentEditMixin, generic.UpdateView):
    submit_label = 'Сохранить'


class StudentDelete(StudentEditMixin, generic.DeleteView):
    submit_label = 'Удалить'


class GroupCreate(GroupEditMixin, generic.CreateView):
    submit_label = 'Добавить'

    def get_action_url(self):
        return reverse('add_group')


class GroupUpdate(StoreOldFieldsValuesMixin, GroupEditMixin, generic.UpdateView):
    submit_label = 'Сохранить'


class GroupDelete(GroupEditMixin, generic.DeleteView):
    submit_label = 'Удалить'
