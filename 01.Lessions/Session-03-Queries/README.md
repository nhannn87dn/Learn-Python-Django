
# Session 04 - Queries

Cách truy vấn dữ liệu thông qua Model trong Django.

Trong bài học trước bạn đã biết cách: INSERT, UPDATE, DELETE và SELECT cơ bản.

Dưới đây là chi tiết hơn về SELECT trong Django Model


## 💛 Truy vấn cơ bản

Tất cả ví dụ dưới đây thao tác trên `shell`

Bạn có thể sử dụng các phương thức có trong `QuerySet` để thực hiện truy vấn

Danh sách phương thức xem: https://docs.djangoproject.com/en/5.0/ref/models/querysets/

Trong Django, bạn có thể xem câu lệnh SQL được tạo ra từ một `QuerySet` bằng cách sử dụng phương thức `query`. Dưới đây là cách bạn có thể thực hiện điều này:

```python
# Tạo một QuerySet
queryset = Product.objects.all() # trả về một danh sách các đối tượng Product
#Hoặc
queryset = Product.objects.all().values() # trả về một danh sách các từ điển, mỗi từ điển chứa các trường của đối tượng Product

# In câu lệnh SQL
print(str(queryset.query))
```

Trong đoạn mã trên, `str(queryset.query)` sẽ trả về một chuỗi chứa câu lệnh SQL tương ứng với `QuerySet`.


Ngoài ra, bạn cũng có thể sử dụng các công cụ như Django Debug Toolbar để xem tất cả các câu lệnh SQL được thực thi trong quá trình xử lý một yêu cầu.


### 🔥 SELECT *

```sql
SELECT * FROM products
```

Sẽ tương đương với

```bash
 all_products = Product.objects.all() #Enter
```


Có sắp xếp order by

```python
products = Product.objects.all().order_by('price')
```

### 🔥 SELECT column_name

```sql
SELECT product_name, price FROM products
```

Sẽ tương đương với

```python
# Lấy tất cả các sản phẩm, nhưng chỉ lấy trường 'product_name' và 'price'
 products = Product.objects.values('product_name', 'price')

# Hoặc sử dụng `values_list()` nếu bạn chỉ muốn kết quả là một danh sách các giá trị thay vì một danh sách các từ điển
 products = Product.objects.values_list('product_name', 'price')
```


### 🔥 SELECT với WHERE

Đi kèm với WHERE là các toán tử để bạn đưa ra điều kiện tìm kiếm.


Ví dụ 1: Lấy sản phẩm có id là 1

```python
# SELECT * FROM products WHERE id = 1
 product = Product.objects.get(id=1)
 product = Product.objects.get(pk=1)
```

Hoặc sử dụng get_object_or_404() nếu bạn muốn trả về một lỗi 404 khi không tìm thấy đối tượng

```python
from django.shortcuts import get_object_or_404

# Lấy sản phẩm có khóa chính (primary key) là 1, hoặc trả về lỗi 404 nếu không tìm thấy
 product = get_object_or_404(Product, pk=1)
```

Ví dụ 2: Tìm các sản phẩm có giá >= 2000 và model_year = 2016


```python
# SELECT * FROM products WHERE price >= 2000 AND model_year=2016
 products = Product.objects.filter(price__gte=2000, model_year=2016)
```

Ví dụ 3: Tìm các sản phẩm có giá < 1000 HOẶC giá > 2000

Để thực hiện một truy vấn với nhiều điều kiện sử dụng toán tử OR, bạn cần sử dụng Q objects1. Ví dụ:

```python
# SELECT * FROM products WHERE price < 1000 OR price > 2000
from django.db.models import Q
products = Product.objects.filter(Q(price__lt=1000) | Q(price__gt=2000))
```

Ví dụ 4: Tìm các sản phẩm có tên chứa từ 'iphone'

```python
# SELECT * FROM products WHERE product_name LILE '%iphone%'
products = Product.objects.filter(product_name__icontains='iphone')
```
Với `icontains` không phân biệt HOA thường, `contains` có phân biệt.

Xem chi tiết cách sử dụng điều kiện: https://docs.djangoproject.com/en/5.0/ref/models/querysets/#field-lookups


## 💛 Truy vấn nâng cao

### 🔥 GROUP BY

Ví dụ 1: Đếm số lượng sản phẩm trong mỗi danh mục

```python
from django.db.models import Count

categories = Product.objects.values('category').annotate(count=Count('id'))
```

Trong ví dụ trên, Product là một model Django, category là một trường ForeignKey trong model Product liên kết đến model Category, và id là trường khóa chính của model Product. Kết quả truy vấn sẽ là một danh sách các từ điển, mỗi từ điển chứa tên danh mục và số lượng sản phẩm trong danh mục đó.



### 🔥 SELECT từ nhiều TABLE

Xem chi tiết: https://docs.djangoproject.com/en/5.0/ref/models/querysets/#query-related-tools

Ví dụ 1: Tìm sản phẩm có giá >= 2000 và thuộc danh mục có category_id = 4.

```python
'''
SELECT * FROM product AS p
LEFT JOIN category AS c ON c.id = p.id
WHERE p.price >= 2000 AND p.category_id = 4
'''
products = Product.objects.filter(price__gte=2000, category__category_id=4)
```


Ví dụ 2: Lấy thông tin sản phẩm và danh mục

```python
'''
SELECT * FROM product AS p
LEFT JOIN category AS c ON c.id = p.id
'''
products = Product.objects.select_related('category').all()
```

Ví dụ 3: Lấy thông tin sản phẩm và category_name

```python
'''
SELECT 
p.id,
p.product_name,
p.price,
c.category_name
FROM product AS p
LEFT JOIN category AS c ON c.id = p.id
'''
products = Product.objects.all().values('id', 'product_name,', 'price', 'category__name')
```

Hoặc

```python
from django.db.models import F

# Lấy tất cả sản phẩm
products = Product.objects.all()

# Thêm trường category_name từ bảng Category vào queryset
products = products.annotate(category_name=F('category__name'))
```

## 💛 Phân trang


```python
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def listing(request):
    contact_list = Contacts.objects.all()
    paginator = Paginator(contact_list, 25) # Hiển thị 25 liên hệ trên mỗi trang

    page_number = request.GET.get('page')
    try:
        contacts = paginator.page(page_number)
    except PageNotAnInteger:
        # Nếu page không phải là số nguyên, trả về trang đầu tiên
        contacts = paginator.page(1)
    except EmptyPage:
        # Nếu page không có item nào, trả về trang cuối cùng
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'list.html', {'contacts': contacts})

```

## 💛 Một số truy vấn nổi bật khác

Dưới đây là cách sử dụng các phương thức `iterator()`, `latest()`, `earliest()`, `first()`, và `last()` trong Django kèm theo ví dụ minh họa:

1. **iterator()**: Phương thức này trả về một iterator trên kết quả truy vấn. Điều này rất hữu ích khi bạn cần xử lý một lượng lớn dữ liệu mà không muốn lưu trữ tất cả kết quả truy vấn trong bộ nhớ.

```python
# Ví dụ sử dụng iterator()
for book in Book.objects.iterator():
    print(book.title)
```

2. **latest(field_name)**: Phương thức này trả về đối tượng mới nhất trong bảng dựa trên trường đã cho.

```python
# Ví dụ sử dụng latest()
latest_book = Book.objects.latest('publication_date')
print(latest_book.title)
```

3. **earliest(field_name)**: Tương tự như `latest()`, nhưng phương thức này trả về đối tượng sớm nhất dựa trên trường đã cho.

```python
# Ví dụ sử dụng earliest()
earliest_book = Book.objects.earliest('publication_date')
print(earliest_book.title)
```

4. **first()**: Phương thức này trả về đối tượng đầu tiên trong `QuerySet` nếu `QuerySet` không rỗng, ngược lại trả về `None`.

```python
# Ví dụ sử dụng first()
first_book = Book.objects.first()
if first_book is not None:
    print(first_book.title)
```

5. **last()**: Phương thức này trả về đối tượng cuối cùng trong `QuerySet` nếu `QuerySet` không rỗng, ngược lại trả về `None`.

```python
# Ví dụ sử dụng last()
last_book = Book.objects.last()
if last_book is not None:
    print(last_book.title)
```


## 💛 Cơ Chế Lazy (Tìm hiểu thêm)

Trong Django ORM, các truy vấn cơ sở dữ liệu được thực hiện một cách "lười biếng" (lazy). Điều này có nghĩa là các truy vấn không được thực hiện ngay lập tức khi bạn tạo chúng mà chỉ khi bạn thực sự cần dữ liệu.

Thay vào đó, nó chỉ tạo ra một đối tượng `QuerySet` đại diện cho truy vấn đó. Cơ sở dữ liệu chỉ được truy vấn khi bạn thực sự cần dữ liệu, chẳng hạn như khi bạn lặp qua queryset, truy cập vào phần tử của nó, hoặc gọi các phương thức như `list()`, `len()`, hoặc `bool()`.

Cơ chế này giúp tối ưu hóa hiệu suất bằng cách giảm số lượng truy vấn cơ sở dữ liệu không cần thiết.

### Ví Dụ Về Cơ Chế Lazy

Giả sử bạn có một model `Product` như sau:

```python
# models.py

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
```

#### Tạo QuerySet

Khi bạn tạo một queryset, không có truy vấn nào được gửi đến cơ sở dữ liệu:

```python
# views.py

from .models import Product

# Tạo queryset, nhưng chưa truy vấn cơ sở dữ liệu
products = Product.objects.filter(is_active=True)
```

#### Thực Hiện Truy Vấn

Truy vấn chỉ được thực hiện khi bạn thực sự cần dữ liệu. Dưới đây là một số tình huống phổ biến khi truy vấn được thực hiện:

1. **Lặp Qua QuerySet**:

    ```python
    for product in products:
        print(product.name)
    ```

2. **Chuyển QuerySet Thành Danh Sách**:

    ```python
    product_list = list(products)
    ```

3. **Truy Cập Từng Phần Tử**:

    ```python
    first_product = products[0]
    ```

4. **Đếm Số Lượng Phần Tử**:

    ```python
    count = products.count()
    ```

5. **Đánh Giá QuerySet Trong Điều Kiện**:

    ```python
    if products:
        print("Có sản phẩm")
    ```

### Ví Dụ Cụ Thể

Giả sử bạn có một view để hiển thị danh sách sản phẩm:

```python
# views.py

from django.shortcuts import render
from .models import Product

def product_list(request):
    # Tạo queryset nhưng chưa thực hiện truy vấn
    products = Product.objects.filter(is_active=True)
    
    # Truy vấn chỉ được thực hiện khi lặp qua queryset hoặc chuyển thành danh sách
    active_products = list(products)
    
    return render(request, 'product_list.html', {'products': active_products})
```

### Lợi Ích Của Cơ Chế Lazy

1. **Hiệu Suất**: Giảm số lượng truy vấn không cần thiết đến cơ sở dữ liệu, giúp tối ưu hóa hiệu suất.
2. **Linh Hoạt**: Cho phép xây dựng các truy vấn phức tạp một cách tuần tự, chỉ thực hiện truy vấn cuối cùng khi cần thiết.


Để chứng minh rằng Django ORM không thực hiện truy vấn ngay lập tức mà chỉ khi cần thiết (lazy evaluation), bạn có thể sử dụng một trigger trong cơ sở dữ liệu để ghi log thời điểm truy vấn được thực hiện. Dưới đây là một ví dụ về cách tạo một trigger trong PostgreSQL để ghi log mỗi khi có truy vấn thực hiện trên bảng `product`.

### 1. Tạo Bảng Log

Đầu tiên, bạn cần tạo một bảng để ghi log khi trigger được kích hoạt:

```sql
CREATE TABLE query_log (
    id SERIAL PRIMARY KEY,
    action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    operation TEXT,
    query TEXT
);
```

### 2. Tạo Trigger Function

Tiếp theo, bạn tạo một trigger function để ghi log thông tin truy vấn:

```sql
CREATE OR REPLACE FUNCTION log_query() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO query_log (operation, query)
    VALUES (TG_OP, current_query());
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### 3. Tạo Trigger

Sau đó, tạo một trigger để gọi function `log_query` mỗi khi có truy vấn `SELECT` trên bảng `product`:

```sql
CREATE TRIGGER log_select_query
AFTER SELECT ON product
FOR EACH STATEMENT
EXECUTE FUNCTION log_query();
```

### 4. Kiểm Tra Lazy Evaluation

Bây giờ bạn có thể kiểm tra lazy evaluation bằng cách tạo một queryset trong Django và quan sát log:

```python
# views.py

from django.shortcuts import render
from .models import Product

def product_list(request):
    # Tạo queryset nhưng chưa thực hiện truy vấn
    products = Product.objects.filter(is_active=True)
    
    # Đến đây chưa có truy vấn nào được thực hiện
    print("Query chưa thực hiện")

    # Thực hiện truy vấn khi lặp qua queryset
    for product in products:
        print(product.name)
    
    return render(request, 'product_list.html', {'products': products})
```

#### Kiểm Tra Log

Sau khi chạy view, kiểm tra bảng `query_log` để xem log của truy vấn:

```sql
SELECT * FROM query_log;
```

Bạn sẽ thấy rằng log chỉ xuất hiện khi dữ liệu thực sự được truy vấn (khi lặp qua queryset).



## 💛 Homeworks Guide
