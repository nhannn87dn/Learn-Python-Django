
# Session 04 - Django Admin 

Django Admin là một công cụ được tích hợp sẵn trong Django, giúp bạn quản lý dữ liệu một cách hiệu quả. Nó cung cấp một giao diện quản trị cho các model, giúp bạn và những người sử dụng khác có thể thêm, sửa, xoá dữ liệu.

Django Admin cung cấp các tính năng như:
- Quản lý người dùng: Django Admin cho phép bạn quản lý người dùng, nhóm và quyền.
- Quản lý dữ liệu: Django Admin cho phép bạn thực hiện các thao tác trên các model, như thêm mới, chỉnh sửa, xoá.
- Tuỳ biến: Django Admin cho phép bạn tuỳ chỉnh giao diện quản trị, như thay đổi cách hiển thị dữ liệu, thêm các trường tìm kiếm, lọc.


## 💛 Admin site

Để sử dụng Django Admin, bạn cần tạo một tài khoản admin bằng lệnh `createsuperuser`, sau đó bạn có thể truy cập vào giao diện quản trị bằng cách truy cập vào đường dẫn `/admin` trên trang web của bạn.

Đường dẫn trên được cấu hình tại `bikestore/url.py`

```python
urlpatterns = [
    path('', include("home.urls")),
    # đường dẫn đến trang admin
    path('admin/', admin.site.urls), 
    path('categories/', include('categories.urls')),
    
]
```

Truy cập vào bạn sẽ thấy form login như sau

![admin01](img/)

## 💛 Admin User

Để đăng nhập vào được Django Admin bạn phải khởi tạo một tài khoản quản trị có quyền cao nhất (root user)

```bash
#Window
py manage.py createsuperuser
# MAC, Ubuntu
python manage.py createsuperuser
```

Sau đó bạn điền `username`, `email` và `password` để đăng ký Supper User.

Sau khi login sẽ có giao diện Django Admin như sau


## 💛 Admin actions

## 💛 Admin documentation generator