from django.db import models
from product.models import Product
from customer.models import Customer
from staff.models import Staff


class Order(models.Model):
    PENDING = 1
    PROCESSING = 2
    CANCEL = 3
    COMPLETED = 4

    ORDER_STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (CANCEL, 'Cancel'),
        (COMPLETED, 'Completed')
    )

    COD = 1
    CREDIT = 2
    ATM = 3
    CASH = 4

    PAYMENT_TYPE_CHOICES = (
        (COD, 'COD'),
        (CREDIT, 'Credit'),
        (ATM, 'ATM'),
        (CASH, 'Cash')
    )
    order_status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=PENDING)
    order_date = models.DateTimeField(auto_now=True)
    required_date = models.DateTimeField(null=True, blank=True, default=None) # Không yêu cầu điền, mặc định None
    shipped_date = models.DateTimeField(null=True, blank=True, default=None) # Không yêu cầu điền, mặc định None
    order_note = models.CharField(max_length=500, null=True, default=None, blank=True) # Không yêu cầu điền, mặc định None
    shipping_street = models.CharField(max_length=500, null=True)
    shipping_city = models.CharField(max_length=50, null=True)
    shipping_state = models.CharField(max_length=50, null=True)
    payment_type = models.SmallIntegerField(choices=PAYMENT_TYPE_CHOICES, default=COD)
    #order_amount = models.DecimalField(max_digits=18, decimal_places=2)
    # Khóa ngoại liên quan
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # Cho phép null, vì khi tạo mới, chưa có nhân viên nào duyệt đơn cả
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, default=None) #  Không yêu cầu điền, mặc định None
    # created_at timestamp
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    # created_at timestamp
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"Order #{self.id}"

    class Meta:
        db_table = 'bs_orders'
        ordering = ['-id']

# Bảng Order Items
class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=18, decimal_places=2)
    discount = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    def __str__(self):
        return f"Order Item #{self.id}"

    class Meta:
        db_table = 'bs_order_items'
        ordering = ['-id']
        # Danh sách các constraints
        constraints = [
            models.CheckConstraint(check=models.Q(quantity__gte=1), name='ck_order_items_quantity'),
            models.CheckConstraint(check=models.Q(price__gte=0), name='ck_order_items_price'),
            models.CheckConstraint(check=models.Q(discount__gte=0, discount__lte=70), name='ck_order_items_discount'),
        ]