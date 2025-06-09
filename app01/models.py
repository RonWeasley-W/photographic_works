from django.db import models

# Create your models here.


IMAGE_CLASS_CHOICES = (
    (1, "人像摄影"),
    (2, "风光摄影"),
    (3, "纪实摄影"),
    (4, "静物摄影"),
    (5, "街头摄影"),
    (6, "野生动物摄影"),
)


class MyImages(models.Model):
    myimg = models.ImageField(verbose_name='图片', upload_to='img/my_img')
    create_time = models.DateTimeField(verbose_name="上传时间", auto_now_add=True)
    image_name = models.CharField(verbose_name="图片名称", max_length=64, default="NULL")
    image_class = models.SmallIntegerField(verbose_name="摄影类别", choices=IMAGE_CLASS_CHOICES, default=0)
    image_exposure = models.TextField(verbose_name="曝光与光影", default="无")
    image_focus = models.TextField(verbose_name="对焦与清晰度", default="无")
    image_composition = models.TextField(verbose_name="构图与画面结构", default="无")
    image_color = models.TextField(verbose_name="视觉冲击力与美感", default="无")
    image_narrative = models.TextField(verbose_name="叙事性与故事感", default="无")
    image_style = models.TextField(verbose_name="风格与创新", default="无")
    page_view = models.IntegerField(verbose_name="浏览量", default=0)
    numbers_of_likes = models.IntegerField(verbose_name="点赞量", default=0)


    def __str__(self) -> str:
        return self.image_name

