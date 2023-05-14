from django.urls import path,include
from . import views

# 定义一个命名空间，用来区分不同应用之间的链接地址
app_name = 'users_ash'

urlpatterns = [
    path('userLogin/',views.loginAsh,name='loginAsh'),
    path('userRegister/',views.registerAsh,name='registerAsh'),
    path('active/<active_code>',views.active_userAsh,name='active_userAsh'),
     # 找回密码发送邮件页面
    path('forget_pwd/', views.forget_pwdAsh, name='forget_pwdAsh'),  
    path('forget_pwd_url/<active_code>', views.forget_pwd_urlAsh, name='forget_pwd_url'),
    path('user_profile/', views.user_profileAsh, name='user_profile'), 
    path('logout/', views.logout_view, name='logoutAsh'),
    path('editor_users/',views.editor_users,name='editor_users'),
    path('developing/',views.develop,name='developing'),
   
]