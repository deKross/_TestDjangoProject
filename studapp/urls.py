# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from studapp import views

group_uri = r'(?P<group>\w+-\d+\w)'
name_r = r'\w+(-\w+)*'
student_uri = r'(?P<last_name>{0})_' \
               '(?P<first_name>{0})_' \
               '(?P<patronymic>{0})'.format(name_r)

urlpatterns = patterns('',
    url(r'^%s/$' % group_uri, views.GroupDetails.as_view(), name='group'),
    url(r'^add/student/$', views.StudentCreate.as_view(), name='add_student'),
    url(r'^%s/%s/edit/$' % (group_uri, student_uri),
        views.StudentUpdate.as_view(), name='change_student'),

    url(r'^%s/%s/delete/$' % (group_uri, student_uri),
        views.StudentDelete.as_view(), name='delete_student'),

    url(r'^add/group/$', views.GroupCreate.as_view(), name='add_group'),
    url(r'^%s/edit/$' % group_uri,
        views.GroupUpdate.as_view(), name='change_group'),

    url(r'^%s/delete/$' % group_uri,
        views.GroupDelete.as_view(), name='delete_group'),

    url(r'^log/$', views.Log.as_view(), name='studapp_log'),
    url(r'^$', views.GroupsList.as_view(), name='group_list'),
)
