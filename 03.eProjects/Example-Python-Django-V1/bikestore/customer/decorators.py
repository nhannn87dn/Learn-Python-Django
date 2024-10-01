from django.shortcuts import redirect
from django.urls import reverse

'''
Bạn có thể sử dụng CustomerAuthMiddleware
để xác thực cho tất cả url bắt đầu /customer
hoặc sử dụng decorators để linh hoạt hơn cho từng views
'''


def customer_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not hasattr(request, 'customer') or not request.customer:
            return redirect(reverse('customer_login'))
        return view_func(request, *args, **kwargs)
    return wrapper
