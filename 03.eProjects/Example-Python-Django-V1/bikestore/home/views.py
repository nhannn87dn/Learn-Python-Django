from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.mail import EmailMessage
from product.models import Product
from category.models import Category


# Create your views here.
"""
Tạo một hàm = với tên của app đã tạo
"""
def index(request):
    template = loader.get_template('home_index.html')
   
    # Lấy 5 sản phẩm từ danh mục có id là 1
    products_category_1 = Product.objects.filter(
        category_id=1, 
        is_active=True, 
        is_delete=False
    ).order_by('-created_at')[:5]
    
    # Lấy 5 sản phẩm từ danh mục có id là 2
    products_category_2 = Product.objects.filter(
        category_id=2, 
        is_active=True, 
        is_delete=False
    ).order_by('-created_at')[:5]
    
    # Tạo context chứa các biến muốn sử dụng trong template
    context = {
        'categories': {
            'id': 1, 
            'name': 'Mobile'
        },
        'products_category_1': products_category_1,
        'products_category_2': products_category_2,
    }
    
    # có thể dùng HttpResponse
    return HttpResponse(template.render(context, request))
    #return HttpResponse("Hello, world. You're at the Home Page.")

def sendmail(request):
    print('send mail')
    email = EmailMessage(
        subject='Hello Ngoc nhan form Python Django',
        body='<h2>Body <strong>goes</strong> here<h2>',
        from_email='ecshopvietnamese@gmail.com',
        to=['nhannn87@gmail.com'],
        cc=['nhannn@softech.vn'],
      # bcc=['bcc@example.com'],
        reply_to=['ecshopvietnamese@gmail.com'],
    )
    #mặc định body là text/plain
    #Nếu muốn gửi html thì thêm dòng sau
    email.content_subtype = "html"  # Main content is now text/html
    #Đính kèm file
    #email.attach_file("/images/weather_map.png")
    result = email.send() # 1 success, 0 fail
    print('Status Send', result)
    return HttpResponse("Send mail Example.")