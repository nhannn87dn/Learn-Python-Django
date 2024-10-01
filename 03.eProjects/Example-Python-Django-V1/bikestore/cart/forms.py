from django import forms
from customer.models import Customer
from order.models import Order, OrderItem
from product.models import Product
from widgets.widgets import CustomTextInput, CustomEmailInput, CustomRadioSelect
from django.db.models import Q

class CheckoutForm(forms.Form):
    # Lấy thông tin giỏ hàng đưa vào dỏm
    def __init__(self, *args, **kwargs):
        cart_data = kwargs.pop('cart_data', None)
        super(CheckoutForm, self).__init__(*args, **kwargs)

    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)  # Thêm trường ID khách hàng

    # Khai báo các trường cho Form
    first_name = forms.CharField(
        label="First Name",
        min_length=4,
        max_length=100,
        error_messages={
            "min_length": "Tối thiểu 4 kí tự",
            "required": 'Vui lòng điền First Name'
        },
        widget=CustomTextInput()  # Sử dụng custom widget cho trường này

    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=100,
        error_messages={"required": 'Vui lòng điền Last Name'},
        widget=CustomTextInput()
    )
    email = forms.EmailField(
        label="Email",
        max_length=255,
        error_messages={"required": 'Vui lòng điền Email'},
        help_text="Để nhận email xác nhận đơn hàng",
        widget=CustomEmailInput()
    )
    phone = forms.CharField(
        label="Phone",
        min_length=10,
        max_length=20,
        error_messages={"required": 'Vui lòng điền Phone'},
        widget=CustomTextInput()
    )
    street = forms.CharField(
        label="Street",
        max_length=255,
        error_messages={"required": 'Vui lòng điền Street'},
        widget=CustomTextInput()
    )
    city = forms.CharField(
        label="City",
        max_length=100,
        error_messages={"required": 'Vui lòng điền City'},
        widget=CustomTextInput()
    )
    state = forms.CharField(
        label="State",
        max_length=100,
        error_messages={"required": 'Vui lòng điền State'},
        widget=CustomTextInput()
    )
    zip_code = forms.CharField(
        label="ZipCode",
        max_length=10,
        required=False,
        widget=CustomTextInput()
    )
    PAYMENT_CHOICES = (
        ('1', 'COD'),
        ('2', 'Credit'),
        ('3', 'Banking'),
        ('4', 'Cast')
        # Thêm các lựa chọn khác tại đây...
    )

    payment_type = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect,
        #widget=CustomRadioSelect,
        error_messages={
            "required": 'Vui lòng chọn Phương thức thanh toán'
        }
    )

    order_note = forms.CharField(
        label="Order Note",
        max_length=300,
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control"})
    )
