Trong Django, `QuerySet` là một công cụ mạnh mẽ giúp bạn tương tác với cơ sở dữ liệu. Dưới đây là cách bạn có thể sử dụng `QuerySet` để thực hiện các thao tác `SELECT`, `UPDATE`, và `DELETE`:

1. **SELECT**: Để lấy các đối tượng từ cơ sở dữ liệu, bạn có thể sử dụng phương thức `filter()` hoặc `get()`. Ví dụ:
```python
# Lấy tất cả các đối tượng User có last_login là None
users = User.objects.filter(last_login=None)
```
Phương thức `filter()` trả về một `QuerySet` mới chứa các đối tượng thỏa mãn điều kiện⁴.

2. **UPDATE**: Để cập nhật một hoặc nhiều đối tượng, bạn có thể sử dụng phương thức `update()` trên một `QuerySet`. Ví dụ:
```python
# Cập nhật tất cả các đối tượng User có last_login là None, đặt is_active thành False
User.objects.filter(last_login=None).update(is_active=False)
```
Phương thức `update()` cập nhật tất cả các đối tượng trong `QuerySet` dựa trên các tham số được truyền vào¹⁴.

3. **DELETE**: Để xóa một hoặc nhiều đối tượng, bạn có thể sử dụng phương thức `delete()` trên một `QuerySet` hoặc một đối tượng model. Ví dụ:
```python
# Xóa tất cả các đối tượng User có last_login là None
User.objects.filter(last_login=None).delete()
```
Phương thức `delete()` xóa tất cả các đối tượng trong `QuerySet`².

4. **WHERE và các toán tử**: Django hỗ trợ nhiều loại toán tử để bạn có thể tạo ra các điều kiện phức tạp khi truy vấn. Ví dụ, bạn có thể sử dụng `__exact`, `__iexact`, `__contains`, `__icontains`, `__in`, `__gt`, `__gte`, `__lt`, `__lte`, `__startswith`, `__istartswith`, `__endswith`, `__iendswith`³.

Lưu ý: Khi sử dụng `update()` và `delete()`, Django không gọi đến phương thức `save()` hoặc các signals của model. Do đó, nếu bạn có các logic cần được thực thi khi cập nhật hoặc xóa (như các signals), bạn cần xử lý chúng một cách thủ công¹.

Source: Conversation with Bing, 31/1/2024
(1) Update a field for all objects in a Django QuerySet - Koen Woortman. https://koenwoortman.com/python-django-update-field-for-all-objects-in-queryset/.
(2) How to select a record and update it, with a single queryset in Django?. https://stackoverflow.com/questions/2712682/how-to-select-a-record-and-update-it-with-a-single-queryset-in-django.
(3) python - How to run "SELECT FOR UPDATE" for the default "Delete .... https://stackoverflow.com/questions/74857394/how-to-run-select-for-update-for-the-default-delete-selected-in-django-admin.
(4) python - How to run "SELECT FOR UPDATE" instead of "SELECT" when .... https://stackoverflow.com/questions/74807372/how-to-run-select-for-update-instead-of-select-when-changing-and-deleting-da.
(5) undefined. https://docs.djangoproject.com/en/1.9/ref/models/instances/.



Trong Django, bạn có thể sử dụng toán tử logic `and` và `or` để kết hợp các điều kiện khi truy vấn. Dưới đây là một số ví dụ:

1. **Toán tử AND**: Để sử dụng toán tử `and`, bạn chỉ cần thêm nhiều điều kiện vào phương thức `filter()`. Django sẽ tự động áp dụng toán tử `and` cho tất cả các điều kiện². Ví dụ:

```python
# Lấy tất cả các đối tượng User có last_login là None VÀ is_active là True
users = User.objects.filter(last_login=None, is_active=True)
```

2. **Toán tử OR**: Để sử dụng toán tử `or`, bạn cần sử dụng `Q` objects từ `django.db.models`. Ví dụ:

```python
from django.db.models import Q

# Lấy tất cả các đối tượng User có last_login là None HOẶC is_active là True
users = User.objects.filter(Q(last_login=None) | Q(is_active=True))
```

Trong ví dụ trên, dấu `|` được sử dụng để biểu diễn toán tử `or`².

Lưu ý: Khi sử dụng toán tử `and` và `or` cùng một lúc, bạn cần chú ý đến thứ tự ưu tiên của các toán tử. Trong Python, toán tử `and` có độ ưu tiên cao hơn toán tử `or`¹. Tuy nhiên, trong Django, khi bạn kết hợp `Q` objects với toán tử `and` và `or`, Django sẽ thêm dấu ngoặc đơn cho toán tử `and` nhưng không thêm cho toán tử `or`³.

Source: Conversation with Bing, 31/1/2024
(1) Query Expressions in Django (Part I) - Viblo. https://viblo.asia/p/query-expressions-in-django-part-i-aRBvXnbmeWE.
(2) Kiểu dữ liệu Boolean và các toán tử AND OR NOT trong Python. https://topdev.vn/blog/kieu-du-lieu-boolean-va-cac-toan-tu-and-or-not-trong-python/.
(3) Mệnh Đề If Trong Django - Techacademy. https://techacademy.edu.vn/if-trong-django/.
(4) ..and..or.. | Python Cho Người Việt. https://www.vithon.org/2010/01/andor.html.
(5) Toán tử logic, toán tử trên bit và toán tử gán trong C++. https://gochocit.com/ky-thuat-lap-trinh/toan-tu-logic-toan-tu-tren-bit-va-toan-tu-gan-trong-c.