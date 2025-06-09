import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from app01 import models


# Create your views here.
def home(request):

    return render(request, "home.html")

@csrf_exempt
def add(request):
    """
    图片上传页面功能的实现
    使用get获取当前页面，post方法提交图片
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'add.html')
        # print(request.POST.dict())
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    if request.method == 'POST':  # 上传
        print('>>>>>', request.FILES)
        img_obj = request.FILES.get('myimg')
        print('111', dir(img_obj))
        print('222', img_obj.name)
        models.MyImages.objects.create(myimg=img_obj, create_time=formatted_time, image_name="美女", image_class=1, image_level=2, page_view=0)

        return HttpResponse('ok')


