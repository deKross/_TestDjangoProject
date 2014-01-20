# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from studapp.models import Group


class Command(NoArgsCommand):
    help = "Print list of groups and students."

    def handle_noargs(self, **options):
        for group in Group.objects.all():
            self.stdout.write(group.name + '\n')
            for student in group.student_set.all():
                self.stdout.write(u"\t%s\n" % (student))
