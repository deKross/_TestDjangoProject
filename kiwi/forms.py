# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import forms as aforms
from django.contrib.auth.models import User


class UserCreationForm(aforms.UserCreationForm):
    error_messages = aforms.UserCreationForm.error_messages
    error_messages["dublicate_email"] = "Пользователь с данным адресом электронной почты уже существует."
    email = forms.EmailField(label=u"E-mail")

    class Meta(aforms.UserCreationForm.Meta):
        fields = ("username", "email")

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages["dublicate_email"])
