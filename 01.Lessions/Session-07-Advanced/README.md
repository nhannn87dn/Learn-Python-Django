# Session 07 - Advanced

Tìm hiểu một số tính năng nâng cao trong Django, cần thiết cho phát triển ứng dụng web.

Chi tiết: https://docs.djangoproject.com/en/5.0/#common-web-application-tools

## CKEditor


Gặp lỗi: `ImportError: cannot import name 'url' from 'django.conf.urls'`

Đổi thành 

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

## Cache

## Send email

## Sitemaps

