# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.encoding import iri_to_uri
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.conf import settings


ADDITION = 1
CHANGE = 2
DELETION = 3


class Student(models.Model):
    first_name = models.CharField('Имя', max_length=30)
    last_name = models.CharField('Фамилия', max_length=30)
    patronymic = models.CharField('Отчество', max_length=30)
    birth_date = models.DateField('Дата рождения')
    student_id = models.IntegerField('№ студ. билета')
    group = models.ForeignKey('Group', verbose_name='Группа')

    def __unicode__(self):
        return "%s %s %s" % (self.last_name, self.first_name, self.patronymic)

    def get_absolute_url(self):
        return "%s%s/" % (self.group.get_absolute_url(),
                          iri_to_uri('_'.join((self.last_name,
                                               self.first_name,
                                               self.patronymic))))

    def is_praepostor(self):
        return self.group.praepostor == self
    is_praepostor.boolean = True
    is_praepostor.short_description = 'Староста?'


class Group(models.Model):
    name = models.CharField('Название', max_length=10)
    praepostor = models.ForeignKey(Student, related_name='+',
                                   verbose_name='Староста',
                                   null=True, blank=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('group', args=[self.name])

    def students_count(self):
        # return Student.objects.filter(group__id=self).count()
        return self.student_set.count()
    students_count.short_description = 'Кол-во студентов'


class LogEntry(models.Model):
    action_time = models.DateTimeField('action time', auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                             related_name='+')
    object_repr = models.CharField('object repr', max_length=200)
    content_type = models.ForeignKey(ContentType, blank=True, null=True,
                                     related_name='+')
    object_id = models.TextField('object id', blank=True, null=True)
    obj = GenericForeignKey()
    action_flag = models.PositiveSmallIntegerField('action flag')
    data = models.TextField()

    class Meta:
        ordering = ('-action_time',)
        db_table = 'studapp_log'


for cls in (Student, Group):
    @receiver(post_save, sender=cls, weak=False)
    def post_save_cb(sender, instance, created, **kwargs):
        fields = [(i, field.value_from_object(instance))
                  for i, field in enumerate(instance._meta.fields)]
        if not created and hasattr(instance, '_old_fields'):
            fds = []
            for field in fields:
                old = instance._old_fields[field[0]]
                if old != field[1]:
                    fds.append((field[0], "%s%%%%%s" % (old, field[1])))
            fields = fds
        fields = '%%'.join("%d%%%%%s" % field for field in fields)
        LogEntry.objects.create(
                user=getattr(instance, '_commiter', None),
                object_repr=repr(instance)[:200].decode('utf-8'),
                content_type=ContentType.objects.get_for_model(sender),
                object_id=instance.pk,
                action_flag=ADDITION if created else CHANGE,
                data=fields)

    @receiver(post_delete, sender=cls, weak=False)
    def post_delete_cb(sender, instance, **kwargs):
        LogEntry.objects.create(
                user=getattr(instance, '_commiter', None),
                object_repr=repr(instance)[:200].decode('utf-8'),
                content_type=None, object_id=None,
                action_flag=DELETION, data='')
