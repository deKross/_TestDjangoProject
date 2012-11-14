# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import iri_to_uri


class Student(models.Model):
    first_name = models.CharField("Имя", max_length=30)
    last_name = models.CharField("Фамилия", max_length=30)
    patronymic = models.CharField("Отчество", max_length=30)
    birth_date = models.DateField("Дата рождения")
    student_id = models.IntegerField("№ студ. билета")
    group = models.ForeignKey("Group", verbose_name="Группа")

    def __unicode__(self):
        return "%s %s %s" % (self.last_name, self.first_name, self.patronymic)

    def get_absolute_url(self):
        return iri_to_uri("%s%s/" % (self.group.get_absolute_url(), '_'.join((self.last_name, self.first_name, self.patronymic))))

    def is_praepostor(self):
        return self.group.praepostor == self
    is_praepostor.boolean = True
    is_praepostor.short_description = "Староста?"


class Group(models.Model):
    name = models.CharField("Название", max_length=10)
    praepostor = models.ForeignKey(Student, related_name="group2", verbose_name="Староста")

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return iri_to_uri("/%s/" % self.name)

    def students_count(self):
        # return Student.objects.filter(group__id=self).count()
        return self.student_set.count()
    students_count.short_description = "Кол-во студентов"
