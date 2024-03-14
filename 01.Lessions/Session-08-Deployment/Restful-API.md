# Session 08 - Restful API

## 💛 Restful API ?

## 💛 Xây dựng hệ thống Restful API

Sử dụng thư viện `Django REST framework` để xây dựng một hệ thống Restful API nhanh chóng và mạnh mẽ.

![Django REST framework](https://www.django-rest-framework.org/img/logo.png)

Document xem tại: https://www.django-rest-framework.org/

Các bước xây dựng:


### Bước 1 - Cấu hình môi trường

```bash
#Tạo môi trường ảo
>py -m venv .env
#Kích hoạt môi trường ảo
>.env\Scripts\activate.bat
```

### Bước 2 - Cài đặt Django và Django Rest Framework

```bash
>py -m pip install Django
>pip install djangorestframework
```

### Bước 3 - Tạo một dự án Django mới

```bash
django-admin startproject restfulApi
cd restfulApi
```

### Bước 4 - Tạo một ứng dụng

```bash
py manage.py startapp categories
```

### Bước 5 - Cấu hình ứng dụng và thêm DRF vào INSTALLED_APPS

Mở tệp `restfulApi/settings.py` trong thư mục dự án của bạn và thêm 'rest_framework' vào danh sách `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'categories',  # Thay thế 'home' bằng tên ứng dụng của bạn
]
```

Tiếp theo bạn cấu hình Database.

Tạo mới một `database postgres` có tên `DjangoAPI` trong pgadmin4. Sau đó cấu hình biến `DATABASES` thành như sau.

```python
## Và cấu hình Database
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "DjangoAPI",
        "USER": "postgres",
        "PASSWORD": "123456789",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

### Bước 6 - Tạo model cho API của bạn

Định nghĩa model của bạn trong tệp `models.py` của ứng dụng của bạn

```python
# categories/models.py
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

```

### Bước 7 - Tạo serializer cho model của bạn

Serializer trong Django REST Framework (DRF) là một thành phần quan trọng giúp chuyển đổi dữ liệu giữa Python và các định dạng khác như JSON, XML, hoặc HTML


Để tạo một serializer cho model “Category”, bạn có thể làm như sau:

```python
# myapp/serializers.py
from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    #Validate cho các trường
    name = serializers.CharField(max_length=100, unique=True)

    class Meta:
        model = Category
        fields = '__all__'

```

### Bước 8 - Tạo viewset cho API của bạn

Viewset là một cách tiện lợi để xây dựng API. Nó cung cấp các phương thức chuẩn để thao tác với dữ liệu, giúp bạn viết ít mã hơn và tăng hiệu suất phát triển.

- **ModelViewSet**: Tạo viewset dựa trên model. Nó bao gồm các phương thức CRUD (Create, Retrieve, Update, Delete) và nhiều tính năng khác.
- **ReadOnlyModelViewSet**: Tương tự như ModelViewSet, nhưng chỉ hỗ trợ các phương thức chỉ đọc (Retrieve và List)

Để tạo một viewset cho tài nguyên “Categories”, bạn có thể làm như sau:

```python
# myapp/views.py
from rest_framework import viewsets
from .models import Category
from .serializers import CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

```

### Bước 9 - Cấu hình router và URL cho API của bạn

Tạo tệp `urls.py` trong ứng dụng của bạn và cấu hình router

```python
# categories/urls.py
from rest_framework import routers
from .views import CategoryViewSet

router = routers.DefaultRouter()
router.register('', CategoryViewSet)

urlpatterns = [
    path('categories/', include(router.urls)),
]
```

Sau đó kết nối `urls` của app với `urls` của Django trong

bạn sửa file `restfulApi/urls.py`

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/',include('categories.urls'))
]
```

Khi đó URL của API categories sẽ là: http://127.0.0.1:8000/api/v1/categories/


### Bước 10 - Migration

```bash
#Để tạo thay đổi cho model categories
py manage.py makemigrations categories
#Thực thi thay đổi
py migrate
```

Django sẽ tạo table của ứng dụng và các table của hệ thống. Bạn có thể check lại cấu trúc table trong database `DjangoAPI`

### Bước 11 - Chạy server và kiểm tra API của bạn


Chạy server bằng lệnh

```bash
py manage.py runserver
```

Truy cập API của bạn tại `http://127.0.0.1:8000/api/v1/categories/`

Bây giờ bạn đã có một API cho tài nguyên “Categories” với các phương thức GET, POST, PUT và DELETE

Điểm mạnh mẽ của `Django REST framework` là toàn bộ CRUD của API `Categories` được tạo tự động sau khi bạn cấu hình như trên.


## 💛 Bảo mật hệ thống

### Authentication and Authorization

### CORs

## 💛 Homeworks Guide

