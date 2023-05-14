from typing import Any, Dict
from django import forms
from django.contrib.auth.models import User
from .models import UserProfileAsh


# 登录表单
class loginFormAsh(forms.Form):
    username = forms.CharField(label="用户名",max_length=32,widget=forms.TextInput(
        attrs={
            'class':'input',
            'placeholder':'用户名/邮箱'
        }
    ))
    password = forms.CharField(label="登录密码",min_length=8,widget=forms.PasswordInput(
        attrs={
            'class':'input',
            'placeholder':'密码'
        }
    ))

    # 自定义验证方法
    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        # 验证用户名与密码不能一致
        if username == password:
            raise forms.ValidationError('用户名与密码不能相同！')
        return password

# 注册表单
class registerFormAsh(forms.ModelForm):
    email = forms.EmailField(label="邮箱",min_length=3,widget=forms.EmailInput(
        attrs={
            'class':'input',
            'placeholder':'邮箱'
        }
    ))
    password = forms.CharField(label="登录密码",min_length=8,widget=forms.PasswordInput(
        attrs={
            'class':'input',
            'placeholder':'密码'
        }
    ))
    password1 = forms.CharField(label="确认登录密码",min_length=8,widget=forms.PasswordInput(
        attrs={
            'class':'input',
            'placeholder':'确认密码'
        }
    ))

    class Meta:
        model = User
        fields = ('email','password')

    # 验证用户名是否已被注册
    def clean_email(self):
        # 获取表单提交的信息
        email = self.cleaned_data.get('email')
        # 验证数据库信息
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError('此邮箱已被注册！')
        return email

    # 验证两次输入的密码是否一致
    def clean_password1(self):
        if self.cleaned_data['password'] != self.cleaned_data['password1']:
            raise forms.ValidationError('两次密码输入不一致！')
        return self.cleaned_data['password1']

# 填写邮箱地址表单 
class forgetPwdFormAsh(forms.Form):
    
    email = forms.EmailField(label='请输入注册邮箱地址', min_length=4, widget=forms.EmailInput(
        attrs={
            'class': 'input', 
            'placeholder': '用户名/邮箱'
        }
    ))

# 修改密码表单
class modifyPwdFormAsh(forms.Form):
	password = forms.CharField(label='输入新密码', min_length=6, widget=forms.PasswordInput(
        attrs={
            'class':'input', 
            'placeholder':'输入新密码'
        }
    ))
        
#  User模型的表单，只允许修改email一个数据，用户名不允许修改 
class UserFormAsh(forms.ModelForm):
    email = forms.EmailField(label="邮箱",min_length=3,widget=forms.EmailInput(
        attrs={
            'class':'input',
            'placeholder':'邮箱'
        }
    ))
    nike_name = forms.CharField(label="昵称",max_length=32,widget=forms.TextInput(
        attrs={
            'class':'input',
            'placeholder':'昵称'
        }
    ))
    signature = forms.CharField(label="个性签名",widget=forms.Textarea(
        attrs={
            'class':'input',
            'placeholder':'个性签名',
            'rows':3
        }
    ))  
    intro = forms.CharField(label="个人简介",widget=forms.Textarea(
        attrs={
            'class':'input',
            'placeholder':'个人简介',
            'rows':5
        }
    ))
    birthday = forms.DateField(label="生日",widget=forms.DateInput(
        attrs={
            'class':'input',
            'placeholder':'生日'
        }
    ))
    address = forms.CharField(label="地址",widget=forms.Textarea(
        attrs={
            'class':'input',
            'placeholder':'地址',
            'rows':3
        }
    ))
    picture = forms.ImageField(label="头像")  
    gender = forms.ChoiceField(label="性别",choices=((0,'女'),(1,'男'),))  
    
    class Meta:
        model = User
        fields = ('email','nike_name','signature','intro','birthday','address','picture','gender')

# UserProfile的表单 
class UserProfileFormAsh(forms.ModelForm):
    
   

    class Meta:
        """Meta definition for UserInfoform."""
        model = UserProfileAsh
        fields = ('nike_name_ash','desc', 'gexing', 'birthday_ash',  'gender_ash', 'address_ash', 'image_ash')
