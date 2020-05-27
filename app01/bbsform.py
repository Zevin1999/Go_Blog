from django import forms
from django.forms import widgets

from django.core.exceptions import ValidationError
#继承Form类
from app01 import models


class RegForm(forms.Form):
    username = forms.CharField(max_length=18, min_length=3, required=True, label="用户名",
                           error_messages={
                                            'max_length': '用户名过长',
                                            'min_length': '用户名过短',
                                            'required': '不能为空'},
                           widget=widgets.TextInput(attrs={'class': 'form-control'}),
                           )
    password = forms.CharField(max_length=18, min_length=3, required=True, label="密码",
                          error_messages={
                               'max_length': '密码过长',
                               'min_length': '密码过短',
                               'required': '不能为空'},
                          widget=widgets.PasswordInput(attrs={'class': 'form-control'}),
                          )
    re_pwd = forms.CharField(max_length=18, min_length=3, required=True, label="确认密码",
                             error_messages={
                              'max_length': '密码过长',
                              'min_length': '密码过短',
                              'required': '不能为空'},
                             widget=widgets.PasswordInput(attrs={'class': 'form-control'}),
                             )
    email = forms.CharField(max_length=18, min_length=3, required=True, label="邮箱",
                            error_messages={
                               'max_length': '邮箱过长',
                               'min_length': '邮箱过短',
                               'required': '不能为空'},
                            widget=widgets.EmailInput(attrs={'class': 'form-control'}),
                            )
   #局部钩子，局部校验
    def clean_username(self):
        # #取出name对应的值
        name = self.cleaned_data.get('username')
        # if name.startwith('s'):
        #     #抛异常
        #     raise ValidationError("不能以s开头")
        # else:
        #     return name
        user = models.UserInfo.objects.filter(username=name).first()
        if user:
            raise ValidationError("用户已存在")
        else:
            return name

    #全局钩子，全局校验
    def clean(self):
        pwd = self.cleaned_data.get('password')
        re_pwd = self.cleaned_data.get('re_pwd')
        if pwd == re_pwd:
            return self.cleaned_data
        else:
            raise ValidationError("两次密码不一致")