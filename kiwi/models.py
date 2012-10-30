# -*- coding: utf-8 -*-
from django.db import models


class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30)
    birth_date = models.DateField()
    student_id = models.IntegerField()
    group = models.ForeignKey("Group")

    def __unicode__(self):
        return "%s %s %s" % (self.last_name, self.first_name, self.patronymic)


class Group(models.Model):
    name = models.CharField(max_length=10)
    praepostor = models.ForeignKey(Student)

    def __unicode__(self):
        return self.name
