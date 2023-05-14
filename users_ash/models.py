from django.db import models
# 引入django内置的一个用户User模型，然后通过一对一关联关系为默认的User拓展用户数据
from django.contrib.auth.models import User

# Create your models here.

# 用户信息表 
class UserProfileAsh(models.Model):

    USER_GENDER_TYPE_ASH = (
        ('male','男'),
        ('female','女'),
    )

    owner = models.OneToOneField(User,on_delete=models.CASCADE,verbose_name='用户')
    # 用户昵称 使用短文本字段 varchar
    nike_name_ash = models.CharField('昵称',max_length=32,blank=True,default='')
    # 用户生日 使用时间字段
    birthday_ash = models.DateField('生日',null=True,blank=True)
    # 用户性别 使用短文本字段
    gender_ash = models.CharField('性别',max_length=6,choices=USER_GENDER_TYPE_ASH,default='male')
    # 用户地址 使用短文本字段
    address_ash = models.CharField('地址',max_length=100,blank=True,default='')
    # 用户头像 ImageFiled字段必须定义upload_to选项，
            # 这个选项用来指定用于上传文件的MEDIA_ROOT的子目录。
            # 例如在blog_for_ash/settings.py中配置了MEDIA_ROOT = os.path.join(BASE_DIR,'media'),
            # 再此设置了upload_to='images/%y/%m',upload_to的'%y/%m/%d'部分是strftime()格式，
            # '%y'是四位数年份，'%m'是二位数月份，'%d'是二位数天数。
            # 如果在2023年7月15日上传文件，它将保存在/media/images/2023/07中
    image_ash = models.ImageField(upload_to='images/%y/%m',default='images/default.png',max_length=100,verbose_name='用户头像')
    desc = models.TextField('个人简介', max_length=200, blank=True, default='')
    gexing = models.CharField('个性签名', max_length=100, blank=True, default='')


    # 设置模型数据的元数据自定义标题
    class Meta:
        verbose_name = '用户数据'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.owner.username,self.image_ash

# 邮箱验证码验证记录
class EmailVerifyRecordAsh(models.Model):
    # 邮箱验证类型
    SEND_TYPE_CHOICES = (
        ('register', '注册'),
        ('forget', '找回密码'),
    )

    code = models.CharField('验证码', max_length=20)
    email = models.EmailField('邮箱', max_length=50)
    # 邮箱验证类型
    send_type = models.CharField(choices=SEND_TYPE_CHOICES, max_length=10, default='register')
    send_time = models.DateTimeField('时间', auto_now_add=True)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
