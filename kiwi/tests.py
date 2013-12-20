#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from django.test import TestCase
from django.contrib.auth.models import User
from kiwi.models import Group, Student


class SimpleTest(TestCase):
    def test_basic_addition(self):
        admin = User.objects.create_superuser('Ben', 'benedict@church.va', 'TheLord')
        self.assertTrue(self.client.login(username='benedict@church.va', password='TheLord'))

        group = Group(name='ТГ-01а')
        group.save()

        response = self.client.get('/')
        self.assertIn(group, response.context['groups'])

        response = self.client.post('/add/student/', {'first_name': 'Karl', 'last_name': 'Dönitz',
                                                      'patronymic': 'FührerDerUBoote',
                                                      'student_id': '39256847',
                                                      'birth_date': '1891-09-16', 'group': group.id})

        self.assertEqual(Student.objects.filter(first_name='Karl').count(), 1)

        response = self.client.post('/add/student/', {'first_name': 'Александр', 'last_name': 'Девятко',
                                                      'patronymic': 'Данилович',
                                                      'student_id': '57086154',
                                                      'birth_date': '1908-06-04', 'group': group.id})

        self.assertEqual(Student.objects.filter(last_name='Девятко').count(), 1)

        response = self.client.post('/ТГ-01а/Dönitz_Karl_FührerDerUBoote/edit/',
                                    {'first_name': 'Карл', 'last_name': 'Дёниц',
                                     'patronymic': 'Кригсмарине',
                                     'student_id': '74865293',
                                     'birth_date': '1891-09-16',
                                     'group': group.id}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Student.objects.filter(last_name='Дёниц').count(), 1)

        response = self.client.post('/ТГ-01а/Девятко_Александр_Данилович/delete/', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Student.objects.filter(group=group).count(), 1)
