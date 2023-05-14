import os
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse # 返回json格式数据
from django.conf import settings 


# 取消掉应用该当前视图的csrf_token验证，也就是说提交数据时不需要csrf_token验证！
@csrf_exempt
def upload_file(request):
    """ ckeditor5图片上传 """
    # 获取表单的上传图片
    upload = request.FILES.get('upload')
    # 生成uuid 
    uid = ''.join(str(uuid.uuid4()).split('-'))
    # 修改图片名称 
    names = str(upload.name).split('.')
    names[0] = uid
    # 拼接图片名
    upload.name = '.'.join(names)
    # 构造上传路径
    new_path = os.path.join(settings.MEDIA_ROOT, 'upload/', upload.name)
    # 上传图片
    with open(new_path, 'wb+') as destination:
        for chunk in upload.chunks():
            destination.write(chunk)

    # 构造要求的数据格式并返回
    filename = upload.name
    url = '/media/upload/' + filename
    retdata = { 'url': url, 
                'uploaded': '1',
                'fileName': filename }
    return JsonResponse(retdata)