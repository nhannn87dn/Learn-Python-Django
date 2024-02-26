# Module django.http

Dưới đây là một số ví dụ về việc sử dụng `HttpResponse` và các lớp con của nó trong Django:

1. **HttpResponse**

```python
from django.http import HttpResponse

def hello_world(request):
    return HttpResponse("<h1>Hello, World!</h1>")
```

Trong ví dụ này, view function `hello_world` trả về một `HttpResponse` chứa nội dung HTML "Hello, World!".

2. **JsonResponse**

```python
from django.http import JsonResponse

def get_data(request):
    data = {"name": "John", "age": 30, "city": "New York"}
    return JsonResponse(data)
```

Trong ví dụ này, view function `get_data` trả về một `JsonResponse` chứa dữ liệu JSON.

3. **HttpResponseRedirect**

```python
from django.http import HttpResponseRedirect

def redirect_view(request):
    return HttpResponseRedirect("/new-url/")
```

Trong ví dụ này, view function `redirect_view` trả về một `HttpResponseRedirect`, chuyển hướng người dùng đến "/new-url/".

4. **HttpResponseNotFound**

```python
from django.http import HttpResponseNotFound

def not_found_view(request):
    return HttpResponseNotFound("<h1>Page not found</h1>")
```

Trong ví dụ này, view function `not_found_view` trả về một `HttpResponseNotFound`, hiển thị thông báo "Page not found" khi người dùng truy cập vào một URL không tồn tại.



5. **HttpResponse với Status Code**

```python
from django.http import HttpResponse

def server_error(request):
    return HttpResponse("Sorry, there was a server error.", status=500)
```

Trong ví dụ này, view function `server_error` trả về một `HttpResponse` với nội dung "Sorry, there was a server error." và mã trạng thái HTTP là 500, đại diện cho lỗi máy chủ.

5. **HttpResponse để Download File**

```python
from django.http import FileResponse

def download_file(request):
    file = open('myfile.txt', 'rb')
    response = FileResponse(file)
    response['Content-Disposition'] = 'attachment; filename="myfile.txt"'
    return response
```

Trong ví dụ này, view function `download_file` trả về một `FileResponse` cho phép người dùng tải về file 'myfile.txt'. `Content-Disposition` header được thiết lập để chỉ định tên file khi tải về.


Dưới đây là một số ví dụ về việc sử dụng `HttpResponse` trong Django để trả về hình ảnh:

6. **HttpResponse với hình ảnh PNG**

```python
from django.http import HttpResponse
from PIL import Image

def secure_image(request, image_path):
    response = HttpResponse(content_type="image/png")
    img = Image.open(image_path)
    img.save(response, 'PNG')
    return response
```

Trong ví dụ này, view function `secure_image` mở một hình ảnh từ `image_path` và sau đó lưu hình ảnh đó vào `HttpResponse` dưới dạng PNG¹.

7. **HttpResponse với hình ảnh JPEG**

```python
from django.http import HttpResponse

def serve_image(request, image_path):
    with open(image_path, "rb") as f:
        return HttpResponse(f.read(), content_type="image/jpeg")
```

Trong ví dụ này, view function `serve_image` mở một hình ảnh JPEG từ `image_path` và sau đó đọc nội dung của file và trả về nó trong một `HttpResponse`¹.

Lưu ý: Trong cả hai ví dụ trên, bạn cần chắc chắn rằng file hình ảnh tồn tại và Django có quyền đọc file đó. Nếu không, bạn sẽ gặp lỗi khi thực hiện request này. Ngoài ra, bạn cũng cần chắc chắn rằng hình ảnh không chứa thông tin nhạy cảm hoặc không phù hợp để chia sẻ với người dùng.
