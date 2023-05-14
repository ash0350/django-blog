from users_ash.models import EmailVerifyRecordAsh
# send_mail是django默认为我们封装的邮件发送方法，这个封装方法可以加快邮件的发送
from django.core.mail import send_mail
# 生成随机字符串
import random
# 生成随机字符串
import string

# 生成邮箱验证码
def random_strAsh(randomlength=8):
    # 生成a-z,A-Z,0-9左右的字符
    chars8 = string.ascii_letters + string.digits
    # 从a-zA-Z0-9生成指定数量的随机字符
    strcode8 = ''.join(random.sample(chars8, randomlength))
    return strcode8

# 将生成的验证码保存到数据库
def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecordAsh()
    code = random_strAsh()
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
 
# 验证码保存之后，把带有验证码的链接发送到注册时的邮箱  
    if send_type == 'register':
        email_title = '博客的注册激活链接'
        email_body = '请点击下面链接激活你的账号：http://127.0.0.1:8000/users/active/{0}'.format(code)

        send_status = send_mail(email_title, email_body, 'ash0350@outlook.com', [email])
        if send_status:
            pass
    elif send_type == 'forget':
        email_title = '密码重置链接'
        email_body = '请点击下面链接修改你的密码：http://127.0.0.1:8000/users/forget_pwd_url/{0}'.format(code)
        
        send_status = send_mail(email_title, email_body, 'ash0350@outlook.com', [email])
        if send_status:
            pass