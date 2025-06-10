from django import forms
from .models import MyImages

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = MyImages
        fields = ['myimg', 'image_class']
        labels = {
            'myimg': '选择图片',
            'image_class': '摄影类别',
        }



