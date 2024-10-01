from django.contrib import admin
from .models import Category
from django.urls import reverse
from django.utils.html import format_html

# Cấu hình các trường hiển thị ở trang danh sách
# Trang: Select categories to change
class CategoryAdmin(admin.ModelAdmin):
    # Các trường hiển thị
    list_display = ("id", "category_name", "description", "is_active", "handle_actions")
    
    #Cột có liên kết link
    list_display_links = ["category_name"]
    
    #Thêm một input để search tên danh mục
    search_fields = ['category_name']
    
    #Định nghĩa cột handle_actions
    def handle_actions(self, category):
        view_url = reverse('admin:category_category_change', args=[category.pk])
        delete_url = reverse('admin:category_category_delete', args=[category.pk])
        return format_html('<a href="{}">Edit</a> | <a href="{}">Delete</a>',  view_url, delete_url)
    # Đăt tên hiển thị cho trường handle_actions
    handle_actions.short_description = 'Actions'

# Register your models here.
admin.site.register(Category,CategoryAdmin)