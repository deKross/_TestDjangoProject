# -*- coding: utf-8 -*-
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.validators import validate_email, ValidationError


class EmailModelBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        try:
            validate_email(username)
        except ValidationError:
            return None
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
