# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'group/(\w+-\d+\w)/$', views.GroupDetails.as_view()),
    url(r'$', views.GroupsList.as_view()),
)
