# Session 06 - Forms

Tìm hiểu về cách sử dụng `Forms` thông qua tạo tính năng giỏ hàng trong Django

## 💛 Giới thiệu về Form

**Django** là một framework phát triển web mã nguồn mở rất phổ biến, và nó cung cấp nhiều công cụ và thư viện hỗ trợ xây dựng các biểu mẫu để nhận dữ liệu từ người dùng trên trang web. Hãy cùng tìm hiểu về **Django forms**:

1. **HTML forms**: Trong HTML, biểu mẫu là tập hợp các phần tử nằm trong thẻ `<form>...</form>`, cho phép người dùng nhập văn bản, chọn tùy chọn, thao tác với các đối tượng, và gửi thông tin về máy chủ. Một biểu mẫu cần xác định hai điểm:
    - **URL**: Địa chỉ nơi dữ liệu sẽ được gửi về.
    - **Phương thức HTTP**: Cách dữ liệu sẽ được gửi đi (thông qua GET hoặc POST).

2. **GET và POST**: Đây là hai phương thức HTTP được sử dụng khi làm việc với biểu mẫu. GET dùng để gửi dữ liệu qua URL, trong khi POST gói gọn dữ liệu và gửi đến máy chủ. POST thường được sử dụng khi thay đổi trạng thái hệ thống (ví dụ: thay đổi cơ sở dữ liệu), còn GET thích hợp cho các yêu cầu không ảnh hưởng đến trạng thái hệ thống.

3. **Forms trong Django**: Django cung cấp lớp `Form` để tạo và xử lý biểu mẫu. Các trường của biểu mẫu được ánh xạ vào các phần tử HTML như `<input>`. Để kết xuất đối tượng trong Django, chúng ta cần:
    - **Lưu đối tượng trong view**.
    - **Chuyển đối tượng vào context của Template**.
    - **Mở rộng thành HTML và sử dụng biến mẫu**.

Django forms giúp đơn giản hóa việc xử lý biểu mẫu và là một phần quan trọng trong việc xây dựng ứng dụng web với Django .


## 💛 Tạo Form trong Django

Với Django, Bạn có thể tạo Form với 2 hình thức

- HTML Form: Trong các template. Bạn phải code nhiều hơn
- Đối tượng Form: Code ít hơn, có validate cơ bản

Xem thêm: https://docs.djangoproject.com/en/5.0/topics/forms/


### 🔥 Bước 1 - Tạo Form

Tạo một file `form.py` tại thư mục app mà bạn muốn tạo form.

```python
from django import forms

class YourForm(forms.Form):
    # 1. Kiểu input text
    username = forms.CharField(label='Username', max_length=100)

    # 2. Kiểu input number
    age = forms.IntegerField(label='Age', min_value=18, max_value=100)

    # 3. Kiểu input email
    email = forms.EmailField(label='Email')

    # 4. Kiểu input password
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    # 5. Kiểu input textarea
    message = forms.CharField(label='Message', widget=forms.Textarea)

    # 6. Kiểu file upload
    avatar = forms.FileField(label='Upload Avatar')

    # 7. Kiểu select options
    country_choices = [
        ('us', 'United States'),
        ('uk', 'United Kingdom'),
        ('ca', 'Canada'),
    ]
    country = forms.ChoiceField(label='Country', choices=country_choices)

    # 8. Kiểu radio
    gender_choices = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    gender = forms.ChoiceField(label='Gender', widget=forms.RadioSelect, choices=gender_choices)

    # 9. Kiểu checkbox
    subscribe = forms.BooleanField(label='Subscribe to newsletter', required=False)

```

### 🔥 Bước 2 - Hiển thị `form` ra Template


Tạo một function, là action mà bạn sẽ gọi để xử lý dữ liệu từ form.


```python
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import YourForm


def actionForm(request):
    # Nếu là POST thì xử lý data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = YourForm(request.POST)
        # Check valid Form
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect("/thanks/")

    # Nếu là GET thì render FORM nhập liệu
    else:
        form = YourForm()

    return render(request, "form_template.html", {"form": form})
```

Trong file `form_template.html`

```django
<form action="/url-to-action/" method="post">
    {% csrf_token %}
    {{ form }}
    <button type="submit">Submit</button>
</form>
```

Để có `url-to-action` bạn cần cấu hình nó ở trong file `urls.py` của app


## 💛 Form Fields

Để tận dụng tính năng tạo form mạnh mẽ từ Django, bạn cần biết danh sách các `Form fields`



### 🔥 Core field arguments

Trong **Django**, các **core field arguments** là các tham số được sử dụng để tùy chỉnh các trường (fields) trong một **form** hoặc một **model**. Dưới đây là một số **core field arguments** quan trọng:

1. **`null`**: Xác định liệu trường có thể chứa giá trị `NULL` trong cơ sở dữ liệu hay không. Ví dụ: `null=True` cho phép trường chứa giá trị `NULL`.

2. **`blank`**: Xác định liệu trường có thể để trống hay không. `blank=True` cho phép trường có thể để trống.

3. **`choices`**: Định nghĩa danh sách các lựa chọn cho trường. Ví dụ: `choices=[('us', 'United States'), ('uk', 'United Kingdom')]`.

4. **`default`**: Xác định giá trị mặc định cho trường.

5. **`max_length`**: Xác định độ dài tối đa của trường văn bản (ví dụ: `max_length=100`).

6. **`required`**: Xác định liệu trường có bắt buộc hay không.

7. **`widget`**: Xác định loại giao diện (widget) để hiển thị trường trong form. Ví dụ: `widget=forms.TextInput(attrs={'class': 'my-input'})`.


Xem thêm: https://docs.djangoproject.com/en/5.0/ref/forms/fields/#core-field-arguments



### 🔥 Built-in Field classes

Danh sách các loại Field được Django dựng sẵn.


Xem thêm: https://docs.djangoproject.com/en/5.0/ref/forms/fields/#built-in-field-classes


## 💛 Validators

Validators thường được sử dụng để kiểm tra tính hợp lệ của dữ liệu nhập vào.

Bạn có thể sử dụng `Validators` để kiểm soát dữ liệu trong logic xử lý ở `views.py`, `models.py` và thậm chí là ở `forms.py`

```python
from django.db import models
from django.core.exceptions import ValidationError

def validate_even(value):
    if value % 2 != 0:
        raise ValidationError("Giá trị %(value)s không phải là số chẵn", params={"value": value})

#models.py
class MyModel(models.Model):
    even_field = models.IntegerField(validators=[validate_even])

#forms.py
from django import forms
class MyForm(forms.Form):
    even_field = forms.IntegerField(validators=[validate_even])

```

### 🔥 Validators dựng sẵn

Dưới đây là một số **Validators** quan trọng trong **Django**:

1. **RegexValidator**:
   - **RegexValidator** kiểm tra xem một chuỗi có khớp với một biểu thức chính quy hay không.
   - Bạn có thể sử dụng nó để kiểm tra định dạng của địa chỉ email, số điện thoại, mã số bưu chính, v.v.
   - Ví dụ:

     ```python
     from django.core.validators import RegexValidator

     phone_validator = RegexValidator(
         regex=r'^\d{10}$',
         message='Số điện thoại không hợp lệ. Vui lòng nhập 10 chữ số.',
     )
     ```

2. **EmailValidator**:
   - **EmailValidator** kiểm tra tính hợp lệ của địa chỉ email.
   - Ví dụ:

     ```python
     from django.core.validators import EmailValidator

     email_validator = EmailValidator(
         message='Địa chỉ email không hợp lệ.',
     )
     ```

3. **URLValidator**:
   - **URLValidator** kiểm tra xem một chuỗi có phải là một địa chỉ URL hợp lệ hay không.
   - Ví dụ:

     ```python
     from django.core.validators import URLValidator

     url_validator = URLValidator(
         message='Địa chỉ URL không hợp lệ.',
     )
     ```

4. **validate_email**:
   - **validate_email** là một hàm kiểm tra tính hợp lệ của địa chỉ email.
   - Ví dụ:

     ```python
     from django.core.validators import validate_email

     try:
         validate_email('example@email.com')
     except ValidationError:
         print('Địa chỉ email không hợp lệ.')
     ```

5. **validate_slug** và **validate_unicode_slug**:
   - **validate_slug** kiểm tra tính hợp lệ của chuỗi slug (chỉ chứa ký tự chữ, số, dấu gạch ngang và dấu gạch dưới).
   - **validate_unicode_slug** tương tự nhưng hỗ trợ các ký tự Unicode.
   - Ví dụ:

     ```python
     from django.core.validators import validate_slug, validate_unicode_slug

     try:
         validate_slug('my-blog-post')
         validate_unicode_slug('my-日本語-post')
     except ValidationError:
         print('Chuỗi không phải là slug hợp lệ.')
     ```

6. **FileExtensionValidator**:
   - **FileExtensionValidator** kiểm tra phần mở rộng của tệp tin.
   - Ví dụ:

     ```python
     from django.core.validators import FileExtensionValidator

     image_extension_validator = FileExtensionValidator(
         allowed_extensions=['jpg', 'png', 'gif'],
         message='Chỉ chấp nhận tệp tin ảnh có phần mở rộng jpg, png hoặc gif.',
     )
     ```


### 🔥 Tạo một Validators



```python
from django.db import models
from django.core.exceptions import ValidationError

#Tự định nghĩa một hàm để xử lý validate
def validate_even(value):
    if value % 2 != 0:
        raise ValidationError("Giá trị %(value)s không phải là số chẵn", params={"value": value})

#models.py
class MyModel(models.Model):
    even_field = models.IntegerField(validators=[validate_even])

#forms.py
from django import forms
class MyForm(forms.Form):
    even_field = forms.IntegerField(validators=[validate_even])

```

Kết luận: Qua đó bạn có thể tự tạo cho mình các cơ chế xử lý `Validators` theo nhu cầu.

## 💛 Session & Cookie

### 🔥 Session

### 🔥 Cookie

## 💛 Messages framework

## 💛 Homeworks Guide

Tạo `Form Checkout`