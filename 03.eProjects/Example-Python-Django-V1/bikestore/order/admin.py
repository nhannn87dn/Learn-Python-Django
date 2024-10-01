from django.contrib import admin
from .models import Order, OrderItem
from django import forms
from django.urls import reverse
from django.utils.html import mark_safe, format_html


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    
class OrderAdmin(admin.ModelAdmin):

    def formatted_order_date(self, obj):
        return obj.order_date.strftime("%d-%m-%Y %H:%M:%S")
    formatted_order_date.short_description = 'Created At'
    
    def customer_email(self, obj):
        return obj.customer.email
    customer_email.short_description = 'Email'

    def customer_phone(self, obj):
        return obj.customer.phone
    customer_phone.short_description = 'Phone'
    
    
    def customer_full_name(self, obj):
        return obj.customer.first_name + ' ' + obj.customer.last_name
    customer_full_name.short_description = 'FullName'
    
    def customer_first_name(self, obj):
        return obj.customer.first_name
    customer_first_name.short_description = 'Customer First Name'

    def customer_last_name(self, obj):
        return obj.customer.last_name
    customer_last_name.short_description = 'Customer Last Name'

    def customer_address(self, obj):
        return f"{obj.customer.street}, {obj.customer.city}, {obj.customer.state}, {obj.customer.zip_code}"
    customer_address.short_description = 'Customer Address'
    
    fieldsets = (
        (None, {
            'fields': ('order_status', 'order_date', 'required_date', 'shipped_date', 'order_note', 'shipping_street', 'shipping_city', 'shipping_state', 'payment_type', 'staff')
        }),
        ('Customer Information', {
            'fields': ('customer', 'customer_email', 'customer_phone', 'customer_first_name', 'customer_last_name', 'customer_address')
        }),
    )

    # Danh sách các trường hiển thị ra danh sách
    list_display = ('id', 'customer_full_name', 'customer_email', 'customer_phone', 'order_status', 'payment_type', 'formatted_order_date', 'handle_actions',)
    
    readonly_fields = ('order_date', 'customer_email', 'customer_phone', 'customer_first_name', 'customer_last_name', 'customer_address', 'customer')
    inlines = [OrderItemInline]
    
    # Không muốn trường này xuất hiện ra Form
    #exclude = ('is_verify', 'otp', )

    # Tìm kiếm theo các trường
    search_fields = ('customer__first_name', 'customer__last_name', 'customer__phone', 'customer__email')
    
    # Cột có liên kết link
    list_display_links = ["id"]

    # Bộ Lọc cho lưới hiển thị
    list_filter = ["order_status", "payment_type"]

    def changelist_view(self, request, extra_context=None):
        self.request = request
        return super().changelist_view(request, extra_context)

    # Định nghĩa cột handle_actions
    def handle_actions(self, Order):
        view_url = reverse('admin:order_order_change', args=[Order.pk])
        delete_url = reverse('admin:order_order_delete', args=[Order.pk])
        # Sử dụng self.request ở đây

        return format_html('<a href="{}">View</a> |  <a href="{}">Delete</a>', view_url,  delete_url)

    # Đăt tên hiển thị cho trường handle_actions
    handle_actions.short_description = 'Actions'


# Register your models here.
admin.site.register(Order, OrderAdmin)
