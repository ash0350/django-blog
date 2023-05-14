from django.contrib import admin
from django.contrib.auth.models import User
# Register your models here.

# /admin/中的用户选项是官方默认通过UserAdmin类注册到后台的，引入次类，后面将会继承这个类
from django.contrib.auth.admin import UserAdmin

# 引入定义的模型
from .models import UserProfileAsh,EmailVerifyRecordAsh

# 必须先通过unregister将User取消关联注册
admin.site.unregister(User)

# 定义关联对象的样式，stackedInline为纵向排列每一行，TabularInline为并排排列
class UserProfileInlineAsh(admin.StackedInline):
    # 关联的模型
    model = UserProfileAsh 

# 关联UserProfileAsh
class UserProfileAdminAsh(UserAdmin):
    inlines = [UserProfileInlineAsh]

# 重新注册User模型
admin.site.register(User,UserProfileAdminAsh)

@admin.register(EmailVerifyRecordAsh)
class EamilVerifyRecordAdmin(admin.ModelAdmin):
    '''Admin View for EamilVerifyRecordAsh'''

    list_display = ('code',)

