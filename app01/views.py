import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from app01.models import MyImages
from app01.llm.moltimodal import Qwenv1

# Create your views here.
def home(request):

    return render(request, "home.html")

@csrf_exempt
def update(request):
    """
    图片上传页面功能的实现
    使用get获取当前页面，post方法提交图片
    :param request:
    :return:
    """
    # 模拟预览数据（未上传时显示）
    preview = {
        'title': '晨光静影',
        'category': '人像摄影作品',
        'tech_rating': '4.8/5',
        'creative_rating': '4.6/5',
        'exposure': '这张照片在曝光处理上显得非常自然和谐...',
    }

    if request.method == 'GET':
        # 修复：传递preview变量到模板
        return render(request, 'update.html', {'preview': preview})

    if request.method == 'POST':  # 上传
        print('>>>>>', request.FILES)
        upload_image = request.FILES.get('myimg')

        if upload_image:
            try:
                # 创建并保存图片对象
                image_obj = MyImages(
                    myimg=upload_image,
                    create_time=datetime.now(),
                    image_name=upload_image.name,
                    image_class=request.POST.get('image_class', 1),
                    image_level=2,  # 示例值，可根据需求修改
                    page_view=0  # 示例值，可根据需求修改
                )
                image_obj.save()

                # 模拟AI分析（实际应用中可替换为真实的分析逻辑）
                image_obj.image_exposure = "曝光处理自然和谐，整体亮度适中..."
                image_obj.save()

                # 重定向到成功页面或当前页面
                return redirect('update')  # 假设URL名称为update

            except Exception as e:
                print(f"Error saving image: {e}")
                return HttpResponse('上传失败：保存图片时出错')
        else:
            return HttpResponse('上传失败：未选择图片')

    # 默认返回上传页面
    return render(request, 'update.html', {'preview': preview})

