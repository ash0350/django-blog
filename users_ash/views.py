from django.shortcuts import render,HttpResponse,redirect
# 引入django自带的登陆方法
from django.contrib.auth import authenticate,login,logout
from .forms import loginFormAsh,registerFormAsh,forgetPwdFormAsh,modifyPwdFormAsh,UserFormAsh, UserProfileFormAsh
# ModelBackend是Django使用的默认身份验证后端，重写这个类让他支持验证邮箱
from django.contrib.auth.backends import ModelBackend
# Q 对象能通过 & 和 | 操作符连接起来。当操作符被用于两个 Q 对象之间时会生成一个新的 Q 对象
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
# Create your views here.
from .models import UserProfileAsh,EmailVerifyRecordAsh
from utils.email_send import send_register_email
from django.contrib.auth.decorators import login_required
from django.contrib import messages


class backendAsh(ModelBackend):
    # 邮箱登陆注册
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):   # 加密明文密码
                return user
        except Exception as e:
            return None


def active_userAsh(request, active_code):
    # 修改用户状态，比对验证码
    all_records = EmailVerifyRecordAsh.objects.filter(code=active_code)
    if all_records:
        for record in all_records:
            email = record.email
            user = User.objects.get(email=email)
            user.is_staff = True
            user.save()
            return HttpResponse('邮箱验证成功')
            
    else:
        return HttpResponse('链接有误！')
    return redirect('users:userLogin')


# 登录视图
def loginAsh(request):

    if request.method != 'POST':
        form = loginFormAsh()
    else:
        form = loginFormAsh(request.POST)
        # 验证获取的数据类型是否正确
        if form.is_valid():
            # 获取表单信息(使用form.cleaned_data获取表单验证通过后的字段)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # 验证用户信息
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                # 登陆成功后跳转到博客首页
                return redirect('blog_ash:index')
            else:
                return HttpResponse('用户名或密码错误！')

    # 定义上下文
    context = {'form':form}
    return render(request,'users_ash/loginAsh.html',context)

# 注册视图
def registerAsh(request):
    if request.method != 'POST':
        form = registerFormAsh()
    else:
        form = registerFormAsh(request.POST)
        if form.is_valid():
            # 获取表单提交的数据并保存到数据库
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data.get('password'))
            # 让username等于邮箱即可
            new_user.username = form.cleaned_data.get('email')
            new_user.save()
            # 发送验证邮件
            send_register_email(form.cleaned_data.get('email','register'))
            return HttpResponse("注册成功！请查看邮箱信息验证账户！")
    context = {'form':form}
    return render(request,'users_ash/registerAsh.html',context)

# 找回密码 
def forget_pwdAsh(request):
    if request.method == 'GET':
        form = forgetPwdFormAsh()
    elif request.method == 'POST':
        form = forgetPwdFormAsh(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            # 验证用户是否存在
            exists = User.objects.filter(email=email).exists()
            if exists:
                # 发送邮件
                send_register_email(email, 'forget')
                return HttpResponse('邮件已经发送，请查收！')
            else:
                return HttpResponse('邮箱还未注册，请前往注册！')

    return render(request, 'users_ash/forgetPwd.html', {'form': form})

# 设置新密码
def forget_pwd_urlAsh(request, active_code):
    if request.method != 'POST':
        form = modifyPwdFormAsh()
    else:
        form = modifyPwdFormAsh(request.POST)
        if form.is_valid():
            record = EmailVerifyRecordAsh.objects.get(code=active_code)
            email = record.email
            user = User.objects.get(email=email)
            user.username = email
            # 将新密码转为哈希值
            user.password = make_password(form.cleaned_data.get('password'))
            user.save()
            
            return HttpResponse('修改成功')
        else:
            return HttpResponse('修改失败')

    return render(request, 'users_ash/resetPwd.html', {'form': form})


 # 设置登录后才能访问，如果没有登陆，就跳转到登录界面
@login_required(login_url='users_ash:loginAsh')  
def user_profileAsh(request):
    user = User.objects.get(username=request.user)
    print(user.email)
    return render(request, 'users_ash/userProfile.html', {'user': user})


# 退出登陆
def logout_view(request):
	logout(request)
	return redirect('users_ash:loginAsh')


# # 编辑用户个人信息
# @login_required(login_url='users:login')
# def editor_users(request):
#     return render(request, 'users/editorUsers.html')


 # 登录之后允许访问   编辑用户信息 
@login_required(login_url='users_ash:loginAsh')  
def editor_users(request):
    
    user = User.objects.get(id=request.user.id)
    
    if request.method == "POST":
        # print(type(user))
        try:
            # userprofile和User之间是一个一对一关系，默认注册的时候是没有数据的，注册成功后，才会在个人中心设置信息
            # 如果user_profile存在
            user_profile = user.userprofileash
            form = UserFormAsh(request.POST, instance=user)
            # 向表单填充默认数据
            user_profile_form = UserProfileFormAsh(request.POST, request.FILES, instance=user_profile)  
            # 验证修改的数据的类型是否正确，保存
            if form.is_valid() and user_profile_form.is_valid():
                form.save()
                user_profile_form.save()
                messages.success(request, '个人信息修改成功!')
                return redirect('users_ash:user_profile')
        # 这里发生错误说明userprofile无数据    
        except UserProfileAsh.DoesNotExist: 
            # 填充默认数据 当前用户  
            form = UserFormAsh(request.POST, instance=user)   
            # 空表单，直接获取空表单的数据保存    
            user_profile_form = UserProfileFormAsh(request.POST, request.FILES)  
            if form.is_valid() and user_profile_form.is_valid():
                
                # commit=False 先不保存，先把数据放在内存中，然后再重新给指定的字段赋值添加进去，提交保存新的数据
                new_user_profile = user_profile_form.save(commit=False)
                new_user_profile.owner = request.user
                new_user_profile.save()
                form.save()
                return redirect('users_ash:user_profile')
    else:
        try:
            user_profile = user.userprofileash
            form = UserFormAsh(instance=user)
            user_profile_form = UserProfileFormAsh(instance=user_profile) 
        except UserProfileAsh.DoesNotExist:
            form = UserFormAsh(instance=user)
            # 显示空表单
            user_profile_form = UserProfileFormAsh()  
    return render(request, 'users_ash/editorUsers.html', locals() )


def develop(request):
    return render(request,'users_ash/developing.html')