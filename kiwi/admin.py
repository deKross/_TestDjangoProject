# -*- coding: utf-8 -*-
from django.contrib import admin
import models


class StudentAdmin(admin.ModelAdmin):
    pass


class StudentInline(admin.TabularInline):
    model = models.Student
    extra = 1


class GroupAdmin(admin.ModelAdmin):
    inlines = [StudentInline]


admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.Group, GroupAdmin)

