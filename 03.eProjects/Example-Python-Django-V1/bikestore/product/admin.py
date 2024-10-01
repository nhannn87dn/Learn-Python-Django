from django import forms
from django.contrib import admin
from .models import Product
from django.utils.html import mark_safe, format_html
from django.urls import reverse
from ckeditor_uploader.widgets import CKEditorUploadingWidget



class ProductForm(forms.ModelForm):
    #Ghi đè lại Form, có sử dụng upload
    description = forms.CharField(widget=CKEditorUploadingWidget)
    
    class Meta:
        model = Product
        fields = '__all__'

       
# Cấu hình các trường hiển thị ở trang danh sách
# Trang: Select products to change
class ProductAdmin(admin.ModelAdmin):
    #Thêm vào để customForm
    form = ProductForm
    #Đăng ký hàm vào biến actions
    actions = ["action_active", "action_inactive", "soft_delete", "restore_recyclebin",]
    # Các trường hiển thị
    list_display = ("id", "product_name", "price", "category_name", "is_active", 'handle_actions',)
    #Cột có liên kết link
    list_display_links = ["product_name"]
    
    #Bộ Lọc cho lưới hiển thị
    list_filter = ["status","is_delete", "is_active"]
    
    #Thêm một input để search tên danh mục
    search_fields = ['product_name'] 
    search_help_text = 'Tìm kiếm theo tên sản phẩm'
    
    # Không muốn trường này xuất hiện ra Form
    #exclude = ('is_delete',)
    
    #Hiển thị hình ảnh Thumbnail đã upload
    readonly_fields = ['thumbnail_preview',]
    
    def changelist_view(self, request, extra_context=None):
        self.request = request
        return super().changelist_view(request, extra_context)
    
    #Định nghĩa cột handle_actions
    def handle_actions(self, product):
        view_url = reverse('admin:product_product_change', args=[product.pk])
        delete_url = reverse('admin:product_product_delete', args=[product.pk])
        # Sử dụng self.request ở đây
        #Chỉ hiển thị khi không phải là giỏ rác
        if self.request.GET.get('is_delete__exact') == '1':
            return ''
        else:
            return format_html('<a href="{}">Edit</a> | <a href="{}">Delete</a>',  view_url, delete_url)
    
    # Đăt tên hiển thị cho trường handle_actions
    handle_actions.short_description = 'Actions'
    
    # Định nghĩa cách lấy dữ liệu cho trường category_name
    def category_name(self, product):
        return product.category.category_name
      # Đặt tiêu đề cột
    category_name.short_description = 'Category Name' 
    
    #Custom lại hiển thị sản phẩm
    # Mặc định show chưa xóa
    # Khi dùng bộ lọc thì có thể show sp đã xóa
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.GET.get('is_delete__exact') == '1':
            return qs.filter(is_delete=True)
        else:
            return qs.filter(is_delete=False)

    # Tùy chỉnh hiển thị thêm hình ảnh đã upload
    def thumbnail_preview(self, obj):
        return mark_safe('''
                     <img height='120' src="{img_url}" alt="{img_alt}" />
                     '''.format(img_url=obj.thumbnail.url, img_alt=obj.product_name))
    thumbnail_preview.short_description = 'Thumbnail Preview'
    
    
    #Định nghĩa hàm xử lý action
    @admin.action(permissions=["change", "delete"],description="Delete selected to recyclebin")
    def soft_delete(self, request, queryset):
        queryset.update(is_delete=True)

    #Định nghĩa hàm xử lý action
    # Khôi phục sản phẩm từ giỏ rác
    @admin.action(permissions=["change"],description="Restore selected to recyclebin")
    def restore_recyclebin(self, request, queryset):
        queryset.update(is_delete=False)
        
    
    #Định nghĩa hàm xử lý action
    @admin.action(permissions=["change"],description="Active selected")
    def action_active(self, request, queryset):
        queryset.update(is_active=True)
        
    #Định nghĩa hàm xử lý action
    @admin.action(permissions=["change"],description="InActive selected")
    def action_inactive(self, request, queryset):
        queryset.update(is_active=False)
    
    #Custom hiển thị danh sách actions
    def get_actions(self, request):
        actions = super().get_actions(request)
        '''
        Nếu đang ở giỏ rác thì không soft_delete
        Mà hiển thị xóa thẳng ra khỏi CSDL
        '''
        if request.GET.get('is_delete__exact') == '1' and "soft_delete" in actions:
            del actions["soft_delete"] #xóa hẳn
            del actions["action_inactive"]
            del actions["action_active"]
                
        if request.GET.get('is_delete__exact') != '1' and "delete_selected" in actions:
            del actions["delete_selected"] #xóa hẳn
            del actions["restore_recyclebin"]
            
        '''
        Nếu đang ở Inactive thì show Active
        và ngược lại
        '''
        if request.GET.get('is_active__exact') == '0' and "action_inactive" in actions:
            del actions["action_inactive"]
        if request.GET.get('is_active__exact') == '1' and "action_active" in actions:
            del actions["action_active"]
        
        return actions
    
    #Tùy biến phân trang cho lưới danh sách
    def get_paginator(self, request, queryset, per_page, orphans=0, allow_empty_first_page=True):
         # Tùy chỉnh số lượng mục trên mỗi trang
        per_page = 15
        return super().get_paginator(request, queryset, per_page, orphans, allow_empty_first_page)
    
# Register your models here.
admin.site.register(Product,ProductAdmin)