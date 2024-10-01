from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.shortcuts import redirect
from .models import Customer

'''
Bạn có thể sử dụng CustomerAuthMiddleware
để xác thực cho tất cả url bắt đầu /customer
hoặc sử dụng decorators để linh hoạt hơn cho từng views
'''

class CustomerAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.customer = None  # Thiết lập mặc định cho thuộc tính customer
        if request.path.startswith('/customer/') or request.path.startswith('/cart/'):
            customer_id = request.session.get('customer_id')
            if customer_id:
                try:
                    customer = Customer.objects.get(id=customer_id)
                    request.customer = customer
                except Customer.DoesNotExist:
                    del request.session['customer_id']

            allowed_paths = [
                reverse('customer_login'),
                reverse('customer_register'),
                reverse('customer_forgot_password'),
                reverse('customer_reset_password'),  # Thêm URL reset password vào đây
            ]
            if not request.customer and request.path.startswith('/customer/') and request.path not in allowed_paths:
                return redirect('customer_login')
