# -*- coding: utf-8 -*-
import json
import datetime
import codecs
import random


APP_NAME = "kiwi"


data = None
with codecs.open("data-for-initial-data.json", 'r', "utf-8") as file:
    data = json.load(file)

output = []
student_pk = 1
group_pk = 0

for group in data.keys():
    group_pk += 1
    output.append({"model": APP_NAME + ".group",
                   "pk": group_pk,
                   "fields": {"name": group, "praepostor": student_pk}})
    for student in data[group]:
        last_name, first_name, patronymic = student[0].split()
        date = datetime.datetime.strptime(student[1], "%d.%m.%Y")
        date = datetime.date(date.year, date.month, date.day).isoformat()
        student_id = random.randint(11111111, 99999999)
        output.append({"model": APP_NAME + ".student",
                       "pk": student_pk,
                       "fields": {"group": group_pk,
                                  "first_name": first_name,
                                  "last_name": last_name,
                                  "patronymic": patronymic,
                                  "birth_date": date,
                                  "student_id": student_id}})
        student_pk += 1

with codecs.open("initial_data.json", 'w', "utf-8") as file:
    json.dump(output, file, ensure_ascii=False, indent=4)
