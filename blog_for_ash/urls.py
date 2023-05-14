"""blog_for_ash URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from utils.upload import upload_file # 富文本编辑器图片上传方法

# 函数include()允许引用其他URLconfs，每当django遇到include()时，
# 它会截断与此项匹配的URL的部分，并将剩余的字符串发送到URLconf以供进一步处理。
# 既可以实现即插即用的效果，可以放在自己想要的任何路径下。


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/',include('users_ash.urls')),
    path('blog/', include('blog_ash.urls')),  # 引入blog的url
    path('uploads/', upload_file, name='uploads') #图片上传url
] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)#配置静态文件url

# 配置用户上传文件url
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


