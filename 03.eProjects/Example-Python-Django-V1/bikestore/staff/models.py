from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin


# Để dễ custom lại việc xác thực người dùng mặc định
# Chúng ta sử dụng table staff, thay vì dùng auth mặc định django
'''
Kế thừa lại đối tượng `AbstractUser` để Staff có những trường mặc định mà Django tạo ra
Ngoài ra mở rộng thêm những trường mà Django mặc định không có
Ví dụ như avatar.
Sau đó bạn có thể thêm nhiều trường khác

Bạn cần thêm biến:

AUTH_USER_MODEL = 'staff.Staff' vào file settings.py

Cài thêm thư viện Pillow vào môi trường ảo
py -m pip install Pillow

'''

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

