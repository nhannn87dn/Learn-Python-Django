# Session 02 - Databases and Model

Trong chương này chúng ta sẽ tìm hiểu về `M`, thành phần đầu tiên trong mô hình `MVT`

## 💛 Cấu hình kết nối Database

### 🔥 Cài đặt Database Engines cho dự án

Mặc định Django set sẵn SQLite, tuy nhiên Django cũng hỗ trợ các Database Engines phổ biến:

- PostgreSQL
- MariaDB
- MySQL
- Oracle

Chúng ta sẽ chọn `PostgreSQL` để cài đặt cho dự án bằng cách.


Sau khi activate môi trường ảo. Cài đặt driver

```bash
pip install psycopg2-binary
```

- **psycopg2-binary** là  một driver cần thiết để làm việc với `PostgreSQL` trong python. Phù hợp để chạy local trong quá trình development.
- **psycopg2** được ưu tiên sử dụng cho môi trường production. Nó cần thêm trình biên dịch C để chạy.



### 🔥 Cấu hình setting.py

Sửa biến `DATABASES` file `bikestore/setting.py` 

```python
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "DjangoPostgres", # Tên database
        "USER": "postgres", # User database
        "PASSWORD": "123456789",  # Pass database
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```


## 💛 Tìm hiểu về Model

Trong Django, Model là một lớp Python đại diện cho một bảng trong cơ sở dữ liệu. Mỗi thuộc tính của model tương ứng với một trường trong bảng cơ sở dữ liệu. Mỗi model thường ánh xạ tới một bảng cơ sở dữ liệu.

Tài liệu về Model: 

- https://docs.djangoproject.com/en/5.0/ref/models/
- https://docs.djangoproject.com/en/5.0/topics/db/models/

Lưu ý quan trọng

Khi bạn `migrate` thì Django sẽ tạo ra các table để phục vụ cho việc xác thực người dùng. Và nếu bạn có nhu cầu mở rộng thì khó khắn cho việc làm thế nào để mở rộng.

Do vậy ngay từ lần `migrate` đầu tiên trong project Django HÃY NÊN làm điều này trước.

==> Custom Model Xác thực

Tương ứng trong mô hình CSDL đã học thì `table staffs` là table để login và đăng nhập cho quản trị viên.

```bash
py manage.py startapp staff
python  manage.py startapp staff
```

### 🔥 Định nghĩa một Model

Custome Model Staff trước, sửa file `staff/models.py`

```python
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

class Staff(AbstractUser, PermissionsMixin):
    class Meta:
        #Đổi tên table thành projectName_table_name
        db_table = 'bs_staffs'
        #Sắp xếp mặc định
        ordering = ['-id', 'first_name']
        
        
    #Để hiện thị tên ở trong list Dashboard
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    avatar = models.ImageField(upload_to='upload/%Y/%m')

```

Cấu hình tập tin `settings.py`

```python
#Đăng ký thêm app Staff vào
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home',
    'staff' # ==> Thêm app staff vào
]

#Bạn cần thêm biến
AUTH_USER_MODEL = 'staff.Staff'
```

Cài thêm thư viện Pillow vào môi trường ảo.

Vì `ImageField` tạo ra cơ chế upload và cần `Pillow` để xử lý hình ảnh.

```bash
py -m pip install Pillow
```

Bạn tạo ra Model `Staff` trước như vậy.

Sau khi `migrate` bạn sẽ thấy Django tạo ra 3 table `bs_staff`, `bs_staffs_groups` và `bs_staffs_user_permissions` thay cho các table mặc định `auth_user`, `auth_groups` và `auth_user_user_permissions`

Chúng ta tìm hiểu về xác thực và phân quyền trong bài học sau.

---

Ví dụ bạn tạo model Category bằng cách sửa file   `category/models.py` thành như sau


```python
from django.db import models

# Create your models here.
class Category(models.Model):
    # Trường category_name
    category_name = models.CharField(max_length=50)
    # Trường description
    description = models.CharField(max_length=500)
```

Khi bạn tạo table thì đồng nghĩa nó cũng tạo table category và đồng bộ vào Database.

Bạn phải chắc chắn rằng đã thêm dòng này vào `INSTALLED_APPS` trong file settings.py

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ##
    'home',
    'staff',
    'category',
]
```

```python
from django.db import models

# Create your models here.
class Category(models.Model):

    # Trường category_name
    category_name = models.CharField(max_length=50)
    # Trường description
    description = models.CharField(max_length=500)
```

Tài liệu để học cách tạo Model với các trường và kiểu dữ liệu:

### 🔥 Field Types

Để biết cách tạo trường kiểu chuỗi, kiểu boolean, kiểu date là gì ...

Xem đầy đủ: https://docs.djangoproject.com/en/5.0/ref/models/fields/#field-types



Ví dụ

```python

    # Định nghĩa khóa chính tự tăng. Nếu không được tạo tự động với tên id
    product_id = models.AutoField(primary_key=True)
    #product_name nvarchar(255) UNIQUE NOT NULL
    product_name = models.CharField(max_length=255, unique=True)
    # brand Có quan hệ với Model Brand
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL)
    # category Có quan hệ với Model Category
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    #model_year SMALLINT NOT NULL
    model_year = models.SmallIntegerField()
    #price DECIMAL(18,2) DEFAULT 0
    price = models.DecimalField(max_digits=18, decimal_places=2, default=0)
  

    #description nvarchar(max) NULL
    description = models.TextField(null=True)
    #created_at timestamp 
    created_at = models.DateTimeField(auto_now_add=True)
    #created_at timestamp  
    updated_at = models.DateTimeField(auto_now=True)
    # is_active BOOLEAN NOT NULL DEFAULT True
    is_active = models.BooleanField(default=True)

    #Trường Upload hình ảnh
    #Cần cài thư viện Pillow
    thumbnail = models.ImageField(upload_to='upload/%Y/%m')

    #Email
    email = models.EmailField(max_length=255, unique=True)

    #Trường upload file
    ## file will be saved to MEDIA_ROOT/uploads/2015/01/30
    # Cần cấu hình biến MEDIA_ROOT
    upload = models.FileField(upload_to="uploads/%Y/%m/%d/")

    #Field chọn từ một danh sách định sẵn
    GENDER_CHOICES = {
        1: 'Female',
        2: 'Male',
        3: 'LGBT'
    }
    gender = models.PositiveSmallIntegerField(default=1, choices=GENDER_CHOICES)
```

Xem thêm về Model: https://docs.djangoproject.com/en/5.0/ref/models/

---

### 🔥 Field Options

Là các tùy chọn của trường như: `Null`, `Not Null`, `Default`, `Unique`, `Primary Key`...

Xem đầy đủ: https://docs.djangoproject.com/en/5.0/ref/models/fields/#field-options


---

## 💛 Migration


Trong Django, `migration` được tạo ra để thực hiện các thay đổi đối với cấu trúc cơ sở dữ liệu của bạn - nói cách khác, nó là cách Django đề xuất để bạn sửa đổi cơ sở dữ liệu của mình theo cách an toàn và kiểm soát.

Mỗi khi bạn thay đổi định nghĩa của `models` trong ứng dụng Django của bạn, Django sẽ tạo ra một `migration` để áp dụng những thay đổi này vào cơ sở dữ liệu. Một `migration` có thể thêm hoặc xóa bảng, tạo hoặc xóa chỉ mục, hoặc thay đổi loại dữ liệu của các trường.

Để tạo `migration`, bạn sẽ sử dụng lệnh `makemigrations`:

```bash
#window
py manage.py makemigrations your_app_label
#MacOS, Ubuntu
python manage.py makemigrations your_app_label
```

Để xem lệnh SQL thuần mà Django sẽ thực hiện thay đổi lên Database thật khi áp dụng một migration cụ thể

```bash
#window
py manage.py sqlmigrate your_app_label migration_name
#MacOS, Ubuntu
python manage.py sqlmigrate your_app_label migration_name
```


 Điều này rất hữu ích nếu bạn muốn hiểu rõ hơn về những thay đổi mà Django sẽ thực hiện trên cơ sở dữ liệu của bạn

Để áp dụng `migration`, bạn sẽ sử dụng lệnh `migrate`:

```bash
#window
py manage.py migrate
#MacOS, Ubuntu
python manage.py migrate
```

Như vậy, `migration` giúp bạn quản lý cấu trúc cơ sở dữ liệu của mình một cách linh hoạt và an toàn. Nếu sai sót bạn có thể khôi phục (rollback) lại trạng thái trước khi thực hiện.



Để hủy một migration trong Django, bạn có thể sử dụng lệnh `migrate` kèm theo tên của ứng dụng và tên của migration mà bạn muốn quay lại trước đó. Cú pháp của lệnh như sau:

```bash
#window
py manage.py migrate your_app_label migration_name
#MacOS, Ubuntu
python manage.py migrate your_app_label migration_name
```


Nếu bạn muốn hủy tất cả các migration của một ứng dụng, bạn có thể chỉ cung cấp tên ứng dụng:

```bash
#window
py manage.py migrate your_app_label zero
#MacOS, Ubuntu
python manage.py migrate your_app_label zero
```

Lưu ý rằng, việc hủy migration có thể gây ra mất dữ liệu nếu migration bạn hủy đã thay đổi cấu trúc cơ sở dữ liệu. Hãy cẩn thận khi sử dụng lệnh này.


Tài liệu:

- makemigrations: https://docs.djangoproject.com/en/5.0/ref/django-admin/#django-admin-makemigrations
- migrate: https://docs.djangoproject.com/en/5.0/ref/django-admin/#migrate


Tiếp nối ví dụ trên bạn nhập lệnh

```bash
#window
py manage.py makemigrations category
#MacOS, Ubuntu
python manage.py makemigrations category
```

Kiểu như bạn đặt tên cho những thay đổi lên model.

Hệ thống sẽ sinh ra một file `category/migrations/0001_initial.py`. Để lưu lại những thay đổi này.

Để áp dụng những thay đổi đó bạn chạy lệnh

```bash
#window
py manage.py migrate
#MacOS, Ubuntu
python manage.py migrate
```

Django sẽ tạo table `category` vào trong Datatabase thật mà đã cấu hình trong `settings.py`


## 💛 Truy vấn Model trên Python Shell

Django cung cấp cho chúng ta một công cụ rất mạnh mẽ là `shell`, thực thi các phương thức của Lớp Model trên môi trường nhanh chóng.

Giúp bạn Debug, xem trước, hoặc tác động lên Database thông qua dòng lệnh.

```bash
#windown
py manage.py shell
#MacOS, Ubuntu
python manage.py shell
```

Sau khi chạy xong bạn sẽ thấy trước con trỏ xuất hiện dấu `>>>`, đây chính là môi trường dòng lệnh của `shell`.

Khi bạn ở `Shell`, thì cùng ngữ cảnh các bạn đang đứng trong app.

Cú pháp lệnh trên `shell` hoàn toàn giống khi bạn thao tác trên app với tập tin `.py`

Ví dụ bạn muốn thao tác với Model `Category` để truy vấn dữ liệu.

Bước 1: Bạn phải nhúng Model cần thao tác vào shell

```bash
>>> from category.models import Category #nhấn Enter
```
Bước 2: Sau đó bạn có thể thao tác với mọi thứ với `Category` và Django đã thiết lập cho nó.

Ví dụ để xem danh sách danh mục đã tạo

```bash
>>> Category.objects.all()
#Kết quả
<QuerySet []>
```

### 🔥 QuerySet là gì ?

Trong Django, QuerySet là một tập hợp các đối tượng từ cơ sở dữ liệu. QuerySet được xây dựng như một danh sách các đối tượngQuerySet giúp bạn dễ dàng lấy dữ liệu bạn thực sự cần, bằng cách cho phép bạn lọc và sắp xếp dữ liệu ở một giai đoạn sớm.

QuerySet là một `Lazy`, vì nó không thực hiện truy vấn cơ sở dữ liệu ngay lập tức khi bạn tạo ra nó.

Thay vào đó, QuerySet chỉ thực hiện truy vấn khi bạn yêu cầu đánh giá nó, ví dụ như khi bạn lặp qua QuerySet hoặc khi bạn gọi một phương thức của nó như .count(), .filter()...

### 🔥 Insert dữ liệu vào Model

Ví dụ để chèn thêm các record mới với table Category

```bash
>>> category = Category(category_name="Mouse", description="Mouse description") #Enter
>>>category.save() #Enter
```

Bạn có thể kiểm tra lại dữ liệu bằng cách

```bash
>>> Category.objects.all().values() #Enter
# Tương đương câu lệnh
# SELECT * FROM category
```



### 🔥 Update dữ liệu cho Model

Ví dụ cập nhật description cho record có id = 4

```bash
>>> c = Category.objects.all()[1] #Enter
```

`c` bây giờ nó đại diện cho dòng dữ liệu `record` có id = 4. Và nó là một object do vậy bạn có thể thay đổi giá trị cho các phần tử của object.

```bash
>>> c.description
#Kết quả
'Mouse description'
```

Bây giờ bạn có thể thay đổi giá trị

```bash
>>> c.description='Mouse description updated' #Enter
>>> c.save() #Enter
```

Bạn có thể kiểm tra lại dữ liệu bằng cách

```bash
>>> Category.objects.all().values() #Enter
```

### 🔥 Xóa dữ liệu vào Model

Tương tự như vậy bạn phải truy cập đến dòng dữ liệu cần xóa sau đó mới thực hiện xóa.

```bash
>>> c = Category.objects.all()[1] #Enter
>>> c.delete() #Enter
```

## 💛 Tính kề thừa Model

Django tổ chức các Model dưới dạng Class OOP do vậy nó sẽ có đặc tính kế thừa của hướng đối tượng.

Ví dụ bạn có Model `customers` và `staff` như sau:

```python
from django.db import models

class Customer(models.Model):
   #Meta cấu hình tùy chọn khác cho Model
    class Meta:
        #Custom lại tên table thành customers
        db_table = 'customers'
    
    #Khai báo các trường
    first_name = models.CharField(max_length=50,null=False,blank=False)
    last_name = models.CharField(max_length=50,null=False,blank=False)
    phone = model.CharField(max_length=20,unique=True)
    email = model.CharField(max_length=150,unique=True)
    street = model.CharField(max_length=255)
    city = model.CharField(max_length=50)
    state = model.CharField(max_length=50)
    zip_code = model.CharField(max_length=5, null=True)

class Staff(models.Model):
   #Meta cấu hình tùy chọn khác cho Model
    class Meta:
        #Custom lại tên table thành staffs
        db_table = 'staffs'
    
    #Khai báo các trường
    first_name = models.CharField(max_length=50,null=False,blank=False)
    last_name = models.CharField(max_length=50,null=False,blank=False)
    phone = model.CharField(max_length=20,unique=True)
    email = model.CharField(max_length=150,unique=True)
    active = model.BooleanField(default=1)

```

Dễ thấy rằng 2 Model trên đều có các trường `first_name`, `last_name`, `phone`, `email`.

Do vậy chúng ta có thể tách ra thành một Model khác rồi sau đó kế thừa để tối ưu được code.


```python
from django.db import models

# Tạo lớp Model Abstract chung


class PersonAbstract(models.Model):
    class Meta:
        #Chỉ định nó là model abstract
        # Nếu không nó sẽ sinh ra table mới trong Database
        abstract = True

    #Khai báo các trường chung
    first_name = models.CharField(max_length=50,null=False,blank=False)
    last_name = models.CharField(max_length=50,null=False,blank=False)
    phone = model.CharField(max_length=20,unique=True)
    email = model.CharField(max_length=150,unique=True)

# Kế thừa lại PersonAbstract
class Customer(PersonAbstract):  
    class Meta:
        #Custom lại tên table thành customers
        db_table = 'customers'
    
    #Giữ lại các trường riêng 
    street = model.CharField(max_length=255)
    city = model.CharField(max_length=50)
    state = model.CharField(max_length=50)
    zip_code = model.CharField(max_length=5, null=True)

# Kế thừa lại PersonAbstract
class Staff(PersonAbstract):
   #Meta cấu hình tùy chọn khác cho Model
    class Meta:
        #Custom lại tên table thành staffs
        db_table = 'staffs'
    
    #Giữ lại các trường riêng 
    active = model.BooleanField(default=1)

```

## 💛 Meta Model Options

Xem chi tiết: https://docs.djangoproject.com/en/5.0/ref/models/options/

Dưới đây là một số tùy chọn Meta bạn có thể sử dụng trong mô hình Django:

- `abstract`: Nếu `abstract = True`, mô hình này sẽ là một lớp cơ sở trừu tượng.
- `app_label`: Nếu một mô hình được định nghĩa bên ngoài một ứng dụng trong `INSTALLED_APPS`, nó phải khai báo ứng dụng mà nó thuộc về: `app_label = "myapp"`.
- `base_manager_name`: Tên thuộc tính của trình quản lý, ví dụ, 'objects', để sử dụng cho `base_manager` của mô hình.
- `db_table`: Tên của bảng cơ sở dữ liệu để sử dụng cho mô hình: `db_table = "music_album"`.
- `db_table_comment`: Bình luận về bảng cơ sở dữ liệu để sử dụng cho mô hình này. Nó hữu ích để tài liệu hóa các bảng cơ sở dữ liệu cho những người có quyền truy cập trực tiếp vào cơ sở dữ liệu mà có thể không xem mã Django của bạn.
- `db_tablespace`: Tên của không gian bảng cơ sở dữ liệu để sử dụng cho mô hình này.


- `ordering`: Tùy chọn này cho phép bạn chỉ định thứ tự mặc định của các bản ghi được trả về khi bạn truy vấn mô hình. Bạn có thể sắp xếp theo nhiều trường bằng cách sử dụng một tuple hoặc list. Ví dụ: `ordering = ['lastname', '-id']` sẽ sắp xếp kết quả theo `lastname` tăng dần và `id` giảm dần.

- `indexes`: Tùy chọn này cho phép bạn tạo các chỉ mục tùy chỉnh cho một mô hình. Mỗi chỉ mục trong danh sách phải là một thể hiện của `django.db.models.Index`. Ví dụ: `indexes = [models.Index(fields=['last_name', 'first_name', '-date_of_birth'])]` sẽ tạo một chỉ mục trên các trường `last_name`, `first_name` và `date_of_birth` (theo thứ tự giảm dần).

- `unique_together`: Tùy chọn này cho phép bạn đảm bảo rằng một cặp giá trị không bao giờ được lặp lại. Nó nhận một danh sách các tuple, trong đó mỗi tuple chứa các tên trường cần duy nhất. Ví dụ: `unique_together = (("driver", "restaurant"),)` sẽ đảm bảo rằng mỗi cặp giá trị `driver` và `restaurant` là duy nhất trong bảng.

- `index_together`: Tương tự như `unique_together`, nhưng thay vì đảm bảo tính duy nhất, nó tạo các chỉ mục để tối ưu hóa việc truy vấn. Ví dụ: `index_together = (("user", "time"),)` sẽ tạo một chỉ mục trên cặp trường `user` và `time`.

- `constraints`: Tùy chọn này cho phép bạn tạo các ràng buộc tùy chỉnh cho mô hình. Mỗi ràng buộc trong danh sách phải là một thể hiện của `django.db.models.CheckConstraint` hoặc `django.db.models.UniqueConstraint`. Ví dụ: `constraints = [models.CheckConstraint(check=models.Q(age__gte=18), name="age_gte_18")]` sẽ tạo một ràng buộc kiểm tra để đảm bảo rằng `age` luôn lớn hơn hoặc bằng 18.


Ví dụ:

```python
from django.db import models

# Create your models here.
class Category(models.Model):
    class Meta:
        #Đặt tên table
        db_table = 'bs_categories'
        #Cấu hình sắp xếp mặc định
        ordering = ['category_name']

    # Trường category_name
    category_name = models.CharField(max_length=50)
    # Trường description
    description = models.CharField(max_length=500)
```

```python
from django.db import models

class Product(models.Model):
    class Meta:
        #Đặt tên table
        db_table = 'products'
        #Cấu hình sắp xếp mặc định
        ordering = ['-id'] #dấu - trước tên trường là DESC
        #Đánh chỉ mục index
        indexes = [models.Index(fields=['product_name', 'price'])]
        #Chống trùng lặp
        unique_together = (("product_name", "category_id"),)
        # Danh sách các constraints
        constraints = [
            models.CheckConstraint(check=models.Q(price__gte=0), name='ck_products_price'),
            models.CheckConstraint(check=models.Q(discount__gte=0, discount__lte=70), name='ck_products_discount'),
        ]
```

Lưu ý rằng tùy chọn Meta không phải là bắt buộc, và bạn chỉ nên sử dụng chúng khi bạn muốn thay đổi các giá trị mặc định.

Xem thêm về Contraints: https://docs.djangoproject.com/en/5.0/ref/models/constraints/

Xem thêm về Index: https://docs.djangoproject.com/en/5.0/ref/models/indexes/


## 💛 Mối quan hệ giữa các Models


Chi tiết xem: https://docs.djangoproject.com/en/5.0/ref/models/fields/#module-django.db.models.fields.related

Bạn cần nắm các cú pháp để khai báo mối quan hệ giữa các Model trong Django: `many-to-one`, `many-to-many` và `one-to-one`

### 🔥 Many-to-one

Để định nghĩa quan hệ Many-to-one, bạn sử dụng `django.db.models.ForeignKey` khi báo trường đó trong Model

Lớp này cần đối số:

- model: Model cần tham chiếu tới
- on_delete: Hành động thực hiện cho dòng dữ liệu của table CON khi CHA bị XÓA

Các trường `ForeignKey` sẽ được đánh index tự động (db_index=True)
Khi thực hiện  `mirgate` để tạo CSDL thì Django tự động thêm đuôi _id vào tên trường ForeignKey. Ví dụ: category, dưới CDSL sẽ là category_id.


```python

from django.db import models


class Category(models.Model):
    # ...
    pass

class Product(models.Model):
    # ...
    # brand Có quan hệ với Model Brand
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL,related_name='products_brand')
    # category Có quan hệ với Model Category
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products_category')
```

Lưu ý: Mặc dù bạn sử dụng tên là `category` nhưng khi tạo database django sẽ nối thành `category_id`

Trong đó `on_delete` sẽ có các tùy chọn:

- models.CASCADE
- models.SET_NULL
- models.PROTECT
- models.RESTRICT
- models.SET_DEFAULT
- models.SET
- models.DO_NOTHING

#### related_name

Trong đó `related_name` là một tùy chọn bạn có thể đặt cho một trường ForeignKey. Nó cung cấp một cách để truy cập từ mô hình liên kết (được tham chiếu bởi ForeignKey) trở lại mô hình ban đầu.

Nếu bạn không chỉ định `related_name`, Django sẽ tự động tạo ra một tên bằng cách sử dụng tên của mô hình của bạn với hậu tố `_set`

Ví dụ: Model `Products` có khóa ngoại đến `Category`, bạn có thể lấy tất cả sản phẩm của một danh mục bằng cách: `category.product_set.all()`

Nhưng nếu bạn chỉ định `related_name`. Ví dụ: `related_name='products_category'`, bạn có thể lấy với `category.products_category.all()`

#### related_query_name

Trong Django, `related_query_name` là một tùy chọn bạn có thể đặt cho một trường `ForeignKey`. Nó cung cấp một tên để sử dụng khi thực hiện các truy vấn liên quan từ mô hình liên kết (được tham chiếu bởi `ForeignKey`) trở lại mô hình ban đầu.

Nếu bạn không chỉ định `related_query_name`, Django sẽ tự động tạo ra một tên bằng cách sử dụng tên của mô hình của bạn với hậu tố `_set`.

Ví dụ, nếu bạn có một mô hình `User` và một mô hình `Article` với một trường `ForeignKey` đến `User`, bạn có thể truy cập tất cả các bài viết của một người dùng bằng cách sử dụng `user.article_set.all()`.

Nếu bạn chỉ định `related_query_name`, ví dụ `related_query_name='articles'`, thì bạn có thể truy cập tất cả các bài viết của một người dùng bằng cách sử dụng `User.objects.filter(articles__published_date__year=2023)` để lấy tất cả người dùng đã xuất bản một bài viết trong năm 2023.


### 🔥 Many-to-Many


Trong Django, mối quan hệ nhiều-nhiều (Many-to-many) giữa hai mô hình được tạo ra bằng cách sử dụng trường `ManyToManyField`

Ví dụ: Chúng ta có `Products` có quan hệ Many-to-Many với `Orders`. 1 Sản phẩm có thể thuộc nhiều đơn hàng, và 1 đơn hàng có thể có nhiều sản phẩm.

```python
from django.db import models

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)

class Order(models.Model):
    #...
    order_date = models.DateField(),
    products = models.ManyToManyField(Product)
```

Khi bạn set như vậy thì Django tự động tạo thêm một table `product_order` làm bảng trung gian  với 2 khóa ngoại là product_id, order_id để thể hiện quan hệ `many-to-many`

Tuy nhiên, trong mô hình bán hàng. Table `product_order` cần thêm cột `quantity`, `price`... để mở rộng thông tin. Do vậy Django cung cấp cho bạn một cách thức để mở rộng bằng cách sử dụng tùy chọn `through`


```python
from django.db import models

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)

class Order(models.Model):
    #...
    order_date = models.DateField()
    products = models.ManyToManyField(Product, through='OrderItem')

#Custom Model quan hệ Many-to-Many
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    # Các trường mở rộng
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
```

Lưu ý rằng khi bạn sử dụng thuộc tính `through`, Django sẽ không tự động tạo các trường trong bảng trung gian khi bạn thêm các mối quan hệ. Thay vào đó, bạn sẽ cần phải tạo các trường trong `OrderItem` một cách thủ công

---

#### Truy vấn Many-to-Many

Bạn có thể truy vấn các sản phẩm trong một đơn hàng hoặc các đơn hàng mà một sản phẩm là một phần của như sau:

```python
# Lấy tất cả các sản phẩm trong một đơn hàng
order = Order.objects.get(id=1)
products_in_order = order.products.all()

# Lấy tất cả các đơn hàng mà một sản phẩm là một phần của
product = Product.objects.get(id=1)
orders_with_product = product.order_set.all()
```

Một object được Django tự động tạo ra với cú pháp: `model_set` --> order_set


Nhưng nếu bạn đã custom với `through` thì truy vấn thay đổi thành

```python
# Lấy tất cả các sản phẩm trong một đơn hàng cùng với số lượng
order = Order.objects.get(id=1)
product_orders = order.orderitem_set.all()
for product_order in product_orders:
    print(product_order.product.name, product_order.quantity)

# Lấy tất cả các đơn hàng mà một sản phẩm là một phần của cùng với số lượng
product = Product.objects.get(id=1)
product_orders = product.orderitem_set.all()
for product_order in product_orders:
    print(product_order.order.id, product_order.quantity)
```

Django cũng tạo tự động với cú pháp: `throughvalue_set` --> orderitem_set

---

### 🔥 One-to-One

Trong Django, mối quan hệ Một-Một (One-to-One) giữa hai mô hình được tạo ra bằng cách sử dụng trường `OneToOneField`.

Ví dụ, giả sử bạn có hai mô hình là `User` và `UserProfile`, trong đó một địa điểm có thể là một nhà hàng. Bạn có thể tạo mối quan hệ Một-Một giữa chúng như sau:

```python
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField()
```

Trong ví dụ này, trường `user` trong mô hình `UserProfile` là một `OneToOneField` liên kết đến mô hình `User`.

Khi bạn tạo một mối quan hệ Một-Một, Django sẽ tự động tạo một ràng buộc duy nhất trên trường để đảm bảo rằng mỗi đối tượng `User` chỉ có thể liên kết với một đối tượng `UserProfile` duy nhất.

Bạn có thể truy cập đối tượng `User` từ một đối tượng `UserProfile` hoặc ngược lại bằng cách sử dụng tên của mô hình. Ví dụ:

```python
# Truy cập đối tượng User từ một đối tượng UserProfile
profile = UserProfile.objects.get(id=1)
user = profile.user

# Truy cập đối tượng UserProfile từ một đối tượng User
user = User.objects.get(id=1)
profile = user.userprofile

```

Lưu ý rằng khi bạn truy cập một đối tượng từ một mối quan hệ Một-Một, Django sẽ tạo một truy vấn database. Nếu không có đối tượng nào phù hợp, Django sẽ ném ra một ngoại lệ `DoesNotExist`.

Các tùy chọn khác cho `OneToOneField` bao gồm:

- `on_delete`: Đây là một tùy chọn bắt buộc mà bạn phải chỉ định. Nó xác định hành động sẽ xảy ra khi đối tượng mà trường `OneToOneField` liên kết đến bị xóa.
- `primary_key`: Nếu bạn đặt tùy chọn này thành `True`, thì 2 table sẽ chung tên trường khóa chính.
- `related_name`: Tùy chọn này cho phép bạn chỉ định một tên khác để truy cập mối quan hệ từ mô hình liên kết.
- `related_query_name`: Tùy chọn này cho phép bạn đặt một tên khác để sử dụng khi tạo truy vấn liên quan từ mô hình liên kết.
- `limit_choices_to`: Tùy chọn này cho phép bạn giới hạn các đối tượng có thể được chọn khi tạo một mối quan hệ.
- `parent_link`: Nếu bạn đặt tùy chọn này thành `True`, Django sẽ tạo một liên kết ngược từ mô hình con đến mô hình cha trong một mô hình kế thừa.
- `to_field`: Tùy chọn này cho phép bạn chỉ định một trường khác (không phải là khóa chính) để sử dụng làm mục tiêu cho mối quan hệ.



## 💛 Cập nhật thay đổi Models

Mỗi lần bạn thay đổi cấu trúc Model, bạn phải thực hiện tuần tự các lệnh sau để cập nhật thay đổi lên Database

```bash
#Window
py manage.py makemigrations app_name
py manage.py migrate
#MacOS, Ubuntu
python manage.py makemigrations app_name
python manage.py migrate
```

## 💛 Xóa một Model đã tạo

Để xóa một Model đã định nghĩa trong Django, bạn cần thực hiện các bước sau:

1. Đảm bảo không có app nào đang sử dụng model này nữa
2. Xóa hoặc comment out class Model tương ứng trong file `models.py`.
3. Chạy lệnh `makemigrations` để tạo ra migration mới:

```bash
python manage.py makemigrations
```

4. Chạy lệnh `migrate` để áp dụng các thay đổi vào cơ sở dữ liệu:

```bash
python manage.py migrate
```


Lưu ý rằng, việc xóa một Model sẽ xóa bảng tương ứng trong cơ sở dữ liệu, do đó tất cả dữ liệu trong bảng đó cũng sẽ bị xóa. Nếu bạn muốn giữ lại dữ liệu, hãy sao lưu cơ sở dữ liệu trước khi xóa Model.

Ngoài ra, nếu Model bạn muốn xóa có mối quan hệ với các Model khác thông qua ForeignKey hoặc các trường quan hệ khác, bạn cần xử lý những mối quan hệ này trước khi xóa Model. Cách tiếp cận phụ thuộc vào yêu cầu cụ thể của ứng dụng của bạn.


## 💛 Homeworks Guide

Thực hành tạo các Model

- brands
- products
- customers
- stores
- staffs
- orders
- order_items
- stocks
