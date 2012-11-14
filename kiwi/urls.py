# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^(\w+-\d+\w)/$', views.GroupDetails.as_view()),
    url(r'^add/student/$', views.StudentCreate.as_view()),
    url(r'^(\w+-\d+\w)/(\w+_\w+_\w+)/edit/$', views.StudentUpdate.as_view()),
    url(r'^(\w+-\d+\w)/(\w+_\w+_\w+)/delete/$', views.StudentDelete.as_view()),
    url(r'^$', views.GroupsList.as_view()),
)
