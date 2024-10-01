"""
URL configuration for bikestore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf.urls import include
from django.urls import re_path, path
# Cấu hình đường dẫn static
from django.conf import settings
from django.conf.urls.static import static

"""
Import Tất cả các App vào đây
path(url, include)
url: là route
include: là nạp app vào để hiển thị cho URL đó
"""
urlpatterns = [
    path('', include("home.urls")),  # trang chủ
    path('admin/', admin.site.urls),  # trang admin
    path('products/', include('product.urls')),  # trang sản phẩm
    path('customer/', include('customer.urls')),  # trang khách hàng
    path('cart/', include('cart.urls')),  # trang giỏ hàng
    re_path(r'ckeditor/', include('ckeditor_uploader.urls')),
]

"""
path(route, view, kwargs=None, name=None)

- route là một chuỗi chứa một URL mẫu.
- view khi Django tìm thấy một URL phù hợp, nó sẽ gọi hàm view tương ứng với yêu cầu HTTP đó.
- kwargs là các tham số tùy chọn sẽ được truyền vào view.
- name giúp bạn đặt tên cho URL để bạn có thể tham chiếu đến nó sau này.
"""

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
