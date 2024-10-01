from django.db import models
from django.utils.text import slugify
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password

def get_upload_to(instance, filename):
    # Tạo slug từ product_name hoặc sử dụng trường slug
    slug = slugify(instance.first_name+instance.id)
    # Lấy năm và tháng hiện tại
    year = datetime.now().strftime('%Y')
    month = datetime.now().strftime('%m')
    # Lấy phần mở rộng của tệp
    ext = filename.split('.')[-1]
    # Tạo tên mới cho tệp
    new_filename = '{}/{}/{}.{}'.format(year, month, slug, ext)
    return 'customer/{}'.format(new_filename)


class Customer(models.Model):
    
    # === START TẠO TÙY CHỈNH XÁC THỰC ======
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @property
    def is_authenticated(self):
        return True

    # Để hiện thị tên ở trong list Dashboard
    def __str__(self):
        return self.first_name + ' ' + self.last_name

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=12)
    email = models.EmailField(max_length=150, unique=True)
    birthday = models.DateField(null=True, blank=True, default=None)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10, null=True, blank=True, default=None)
    # created_at timestamp
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    # created_at timestamp
    updated_at = models.DateTimeField(auto_now=True, null=True)
    # is_active BOOLEAN NOT NULL DEFAULT FALSE
    is_active = models.BooleanField(default=True, help_text='Chọn nếu cho phép người dùng hoạt động')
    #Mật khẩu, chưa băm
    is_verify = models.BooleanField(default=False) # xác nhận email
    password = models.CharField(max_length=255, default=None, null=True, blank=True)
    otp = models.CharField(max_length=10, default=None, null=True, blank=True)
    # Hình đại diện
    avatar = models.ImageField(upload_to=get_upload_to, null=True, blank=True, default=None,
                                  help_text='Kích thước 300x300px')

    class Meta:
        db_table = 'bs_customers'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(fields=['email'], name='uq_customers_email'),
        ]