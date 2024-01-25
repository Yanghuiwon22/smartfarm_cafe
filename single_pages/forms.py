from django import forms
from django.contrib.auth.forms import UserCreationForm, BaseUserCreationForm
from django.contrib.auth import get_user_model
from django.db import models



class CustomUserCreationForm(BaseUserCreationForm):
    # student_number = models.IntegerField()

    class Meta:
        model = get_user_model()
        fields = ['student_number','username', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")

        # 비밀번호 길이를 검증하고 조건을 만족하지 않으면 ValidationError을 발생시킵니다.
        if len(password1) < 8:
            raise forms.ValidationError("비밀번호는 최소 8자 이상이어야 합니다.")

        return password2

    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #
    #     if username in
    #
    #     return username
