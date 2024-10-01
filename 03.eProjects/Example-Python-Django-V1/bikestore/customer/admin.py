from django.contrib import admin
from .models import Customer
from django import forms
from django.urls import reverse
from django.utils.html import mark_safe, format_html


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class CustomerAdmin(admin.ModelAdmin):

    # Định nghĩa cách lấy dữ liệu cho trường full_name
    def full_name(self, customer):
        return customer.first_name + ' ' + customer.last_name

    # Đặt tiêu đề cột
    full_name.short_description = 'Fullname'

    def formatted_created_at(self, obj):
        return obj.created_at.strftime("%d-%m-%Y %H:%M:%S")

    formatted_created_at.short_description = 'Created At'

    # Danh sách các trường hiển thị ra danh sách
    list_display = ('full_name', 'email', 'phone', "is_active", 'formatted_created_at', 'handle_actions',)
    # Không muốn trường này xuất hiện ra Form
    exclude = ('is_verify', 'otp', )

    search_fields = ('first_name', 'last_name', 'email', 'phone')
    # Cột có liên kết link
    list_display_links = ["full_name"]

    # Bộ Lọc cho lưới hiển thị
    list_filter = ["is_active",]

    def changelist_view(self, request, extra_context=None):
        self.request = request
        return super().changelist_view(request, extra_context)

    # Định nghĩa cột handle_actions
    def handle_actions(self, customer):
        view_url = reverse('admin:customer_customer_change', args=[customer.pk])
        delete_url = reverse('admin:customer_customer_delete', args=[customer.pk])
        # Sử dụng self.request ở đây

        return format_html('<a href="{}">Edit</a> | <a href="{}">Delete</a>', view_url, delete_url)

    # Đăt tên hiển thị cho trường handle_actions
    handle_actions.short_description = 'Actions'



# Register your models here.
admin.site.register(Customer,CustomerAdmin)