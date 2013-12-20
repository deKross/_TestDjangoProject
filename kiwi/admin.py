# -*- coding: utf-8 -*-
from django.contrib import admin
import models


class StudentAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "patronymic",
                     "birth_date", "student_id", "group", "is_praepostor")
    search_fields = ("last_name", "first_name", "patronymic")
    date_hierarchy = "birth_date"


class StudentInline(admin.TabularInline):
    model = models.Student
    extra = 1


class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "students_count", "praepostor")
    search_fields = ["name"]
    inlines = [StudentInline]


admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.Group, GroupAdmin)

