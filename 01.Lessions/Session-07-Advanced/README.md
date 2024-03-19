# Session 07 - Advanced

Tìm hiểu một số tính năng nâng cao trong Django, cần thiết cho phát triển ứng dụng web.

Chi tiết: https://docs.djangoproject.com/en/5.0/#common-web-application-tools

## 💛 CKEditor

Tích hợp công cụ soạn thảo vào Django

### Bước 1 - Cài đặt thư viện CKEditor

Thêm gói cài đặt `django-ckeditor` cho môi trường ảo

```bash
>pip install django-ckeditor
```

### Bước 2 - Cấu hình lại `setting.py`

- Thêm app 'ckeditor' và 'ckeditor_uploader' vào biến `INSTALLED_APPS` trong file setting.py

- Cấu hình các biến cho CKEDITOR. Thêm 2 dòng này vào `settings.py`

```python
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = "ckeditor/"
```

### Bước 4 - Cấu hình URL tĩnh

Trong file `urls.py` thêm dòng này vào

```python
path('ckeditor/', include('ckeditor_uploader.urls')),
```

Sau đó chạy lệnh

```bash
py manage.py collectstatic
```

Để hệ thống tạo các tài nguyên tĩnh cho ckeditor dùng cho toàn bộ project.

Nếu gặp lỗi bạn sẽ fix như sau:

```python
from __future__ import absolute_import
#Thay dòng nay
#from django.django.conf.urls import url
#bằng dòng này
from django.urls import re_path 

from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache

from . import views

urlpatterns = [
    #dòng này
    re_path(r"^upload/", staff_member_required(views.upload), name="ckeditor_upload"),
    #dòng này
    re_path(
        r"^browse/",
        never_cache(staff_member_required(views.browse)),
        name="ckeditor_browse",
    ),
]
```


### Bước 4 - Tích hợp CKeditor vào Filed

Ví dụ trong Model Product, trường `description` đang dùng là TextFiled, như vậy khi nhập liệu nó render ra `textarea`.

Bạn có thể đổi sang dùng bộ soạn thảo ckeditor cho sinh động hơn về định dạng văn bản.

Sửa `product/models.py` tại trường description sửa lại như sau

```python
from ckeditor.fields import RichTextField

class Product(models.Model):
    #...
    #description = models.TextField(null=True, blank=True)
    description = RichTextField()
```

Tiếp theo sửa file `product/admin.py`, custom lại filed description

Thêm Class `ProductForm` vào

```python
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class ProductForm(forms.ModelForm):
    #Ghi đè lại Form, có sử dụng upload hình ảnh
    description = forms.CharField(widget=CKEditorUploadingWidget)
    
    class Meta:
        model = Product
        fields = '__all__'
```

Thêm dòng này vào `ProductAdmin`

```python
class ProductAdmin(admin.ModelAdmin):
    #Thêm vào để customForm
    form = ProductForm
```

Check lại màn hình chỉnh sửa Product bạn sẽ thấy khung soạn thảo ckeditor.

## 💛 Cache

## 💛 Send email

## 💛 Authentication và Authorization