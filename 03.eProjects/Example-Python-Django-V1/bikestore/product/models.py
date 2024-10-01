from django.db import models
from brand.models import Brand
from category.models import Category
from django.utils.text import slugify
from datetime import datetime
from ckeditor.fields import RichTextField

'''
Tối ưu lại tên tệp tin tải lên
Tối ưu SEO hình ảnh
Đặt hàm này trước Model
'''


def get_upload_to(instance, filename):
    # Tạo slug từ product_name hoặc sử dụng trường slug
    slug = slugify(instance.product_name)
    # Lấy năm và tháng hiện tại
    year = datetime.now().strftime('%Y')
    month = datetime.now().strftime('%m')
    # Lấy phần mở rộng của tệp
    ext = filename.split('.')[-1]
    # Tạo tên mới cho tệp
    new_filename = '{}/{}/{}.{}'.format(year, month, slug, ext)
    return 'products_thumbnail/{}'.format(new_filename)


class Product(models.Model):

    #Để hiện thị tên ở trong list Dashboard
    def __str__(self):
        return self.product_name

    #Custom lại phương thức save()
    def save(self, *args, **kwargs):
        #Tự tạo slug trước khi save
        self.slug = slugify(self.product_name)
        super().save(*args, **kwargs)

    #Custom lại phương thức xóa: Soft Delete
    def delete(self, *args, **kwargs):
        #Xóa sản phẩm, không xóa luôn mà đánh dấu là True ==>
        self.is_delete = True
        self.save()

    # Định nghĩa khóa chính tự tăng. Nếu không được tạo tự động với tên id
    #product_id = models.AutoField(primary_key=True)
    #status Product is a tuples

    STATUS_CHOICES = (
        (1, 'New'),
        (2, 'Old'),
        (3, 'Refurbished'),
        (4, 'Broken'),
    )

    status = models.PositiveSmallIntegerField(default=1, choices=STATUS_CHOICES)

    #product_name nvarchar(255) UNIQUE NOT NULL
    product_name = models.CharField(max_length=255, unique=True, blank=True)
    # 3 trường làm SEO
    slug = models.SlugField(max_length=255, unique=True, null=True, help_text='Ví dụ: iphone-15-pro-max-16gb')
    meta_title = models.CharField(max_length=255, null=True, blank=True, default=None, help_text='Nên nằm trong khoảng 55-70 kí tự')
    meta_description = models.CharField(max_length=255, null=True, blank=True, default=None,
                                        help_text='Nên nằm trong khoảng 155-160 kí tự')
    # brand Có quan hệ với Model Brand
    #on_delete=models.SET_NULL do vậy bạn phải cho phép trường này NULL
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, related_name='brands', null=True)
    # category Có quan hệ với Model Category
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='categories', null=True)
    #model_year SMALLINT NOT NULL
    model_year = models.SmallIntegerField()
    #price DECIMAL(18,2) DEFAULT 0
    price = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    #price DECIMAL(4,2) DEFAULT 0
    discount = models.DecimalField(max_digits=4, decimal_places=2, default=0,
                                   help_text='Chấp nhận giá trị từ 0 - 70 (%)')
    #description nvarchar(max) NULL
    #description = models.TextField(null=True, blank=True)
    description = RichTextField(default=None, null=True, blank=True)
    #created_at timestamp 
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    #created_at timestamp  
    updated_at = models.DateTimeField(auto_now=True, null=True)
    # is_active BOOLEAN NOT NULL DEFAULT FALSE
    is_active = models.BooleanField(default=True, help_text='Chọn nếu sản phẩm đang bán')
    #soft Delete
    is_delete = models.BooleanField(default=False, editable=False)

    #Hình đại diện
    #thumbnail = models.ImageField(upload_to='products_thumbnail/%Y/%m/', null=True,default=None)
    thumbnail = models.ImageField(upload_to=get_upload_to, null=True, blank=True, default=None,
                                  help_text='Kích thước 400x400px')

    class Meta:
        db_table = 'bs_products'
        ordering = ['-id']
        # Danh sách các constraints
        constraints = [
            models.CheckConstraint(check=models.Q(price__gte=0), name='ck_products_price'),
            models.CheckConstraint(check=models.Q(discount__gte=0, discount__lte=70), name='ck_products_discount'),
        ]
