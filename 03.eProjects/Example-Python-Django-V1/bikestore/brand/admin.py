from django.contrib import admin
from .models import Brand
from django.urls import reverse
from django.utils.html import format_html

# Cấu hình các trường hiển thị ở trang danh sách
# Trang: Select brands to change
class BrandAdmin(admin.ModelAdmin):
    # Các trường hiển thị
    list_display = ("id", "brand_name", "description","is_active", "handle_actions")
    
    #Cột có liên kết link
    list_display_links = ["brand_name"]
    
    #Thêm một input để search tên danh mục
    search_fields = ['brand_name']
    
    #Định nghĩa cột handle_actions
    def handle_actions(self, brand):
        view_url = reverse('admin:brand_brand_change', args=[brand.pk])
        delete_url = reverse('admin:brand_brand_delete', args=[brand.pk])
        return format_html('<a href="{}">Edit</a> | <a href="{}">Delete</a>',  view_url, delete_url)
    # Đăt tên hiển thị cho trường handle_actions
    handle_actions.short_description = 'Actions'

# Register your models here.
admin.site.register(Brand,BrandAdmin)