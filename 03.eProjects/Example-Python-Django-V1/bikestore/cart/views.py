from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from .forms import CheckoutForm
from django.contrib import messages
from customer.models import Customer
from order.models import Order, OrderItem
from product.models import Product
#from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q

#@csrf_exempt
@require_http_methods(["DELETE"])
def remove_item_from_cart(request):
    print('remove_item_from_cart')
    try:
        data = json.loads(request.body)
        # Debug
        product_id = data.get('id')

        # Lấy giỏ hàng từ session
        cart = request.session.get('cart', [])

        print('before cart', cart)
        # Xóa sản phẩm ra khỏi giỏ hàng
        # Giữ  lại những phần tử khác với product_id hiện tại.
        new_cart = [item for item in cart if item['id'] != product_id]

        print('after cart', new_cart)

        # Lưu giỏ hàng vào session
        request.session['cart'] = new_cart
        request.session.modified = True  # Đánh dấu session đã được thay đổi

        # reponse to client
        data = {
            'success': True,
            'message': 'Xóa sản phẩm ra khỏi giỏ hàng thành công !',
            'cart': cart
        }
        return JsonResponse(data)

    except Exception as e:  # Bắt lỗi cụ thể
        data = {
            'success': False,
            'message': 'Error: ' + str(e)  # In ra thông điệp lỗi
        }
        return JsonResponse(data)


#@csrf_exempt
@require_http_methods(["DELETE"])
def clear_cart(request):
    print('clear_cart')
    try:
        # Lưu giỏ hàng vào session
        request.session['cart'] = []
        request.session.modified = True  # Đánh dấu session đã được thay đổi

        # reponse to client
        data = {
            'success': True,
            'message': 'Xóa giỏ hàng thành công !'
        }
        return JsonResponse(data)

    except Exception as e:  # Bắt lỗi cụ thể
        data = {
            'success': False,
            'message': 'Error: ' + str(e)  # In ra thông điệp lỗi
        }
        return JsonResponse(data)


#@csrf_exempt  #Bỏ qua kiểm tra CSRF nếu bạn không sử dụng CSRF token
@require_http_methods(["POST"])
def add_to_cart(request):
    try:
        data = json.loads(request.body)
        #Debug
        product_id = data.get('id')
        quantity = data.get('quantity')
        # Lấy giỏ hàng từ session
        cart = request.session.get('cart', [])

        # Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
        for item in cart:
            if item['id'] == product_id:
                # Nếu có, tăng số lượng
                item['quantity'] += quantity
                break
        else:
            # Nếu không, thêm sản phẩm mới vào giỏ hàng
            cart.append({'id': product_id, 'quantity': quantity})

        # Lưu giỏ hàng vào session
        request.session['cart'] = cart
        request.session.modified = True  # Đánh dấu session đã được thay đổi

        #reponse to client
        data = {
            'success': True,
            'message': 'Thêm giỏ hàng thành công !'
        }
        return JsonResponse(data)

    except Exception as e:  # Bắt lỗi cụ thể
        data = {
            'success': False,
            'message': 'Error: ' + str(e)  # In ra thông điệp lỗi
        }
        return JsonResponse(data)


@require_http_methods(["POST"])
def increase_quantity(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('id')

        cart = request.session.get('cart', [])
        for item in cart:
            if item['id'] == product_id:
                item['quantity'] += 1
                break

        request.session['cart'] = cart
        request.session.modified = True  # Đánh dấu session đã được thay đổi

        #reponse to client
        data = {
            'success': True,
            'message': 'Thành công !'
        }
        return JsonResponse(data)
    except Exception as e:  # Bắt lỗi cụ thể
        data = {
            'success': False,
            'message': 'Error: ' + str(e)  # In ra thông điệp lỗi
        }
        return JsonResponse(data)


@require_http_methods(["POST"])
def decrease_quantity(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('id')

        cart = request.session.get('cart', [])
        for item in cart:
            if item['id'] == product_id:
                item['quantity'] = max(0, item['quantity'] - 1)
                break

        request.session['cart'] = cart
        request.session.modified = True  # Đánh dấu session đã được thay đổi

        #reponse to client
        data = {
            'success': True,
            'message': 'Thành công !'
        }
        return JsonResponse(data)
    except Exception as e:  # Bắt lỗi cụ thể
        data = {
            'success': False,
            'message': 'Error: ' + str(e)  # In ra thông điệp lỗi
        }
        return JsonResponse(data)


## Danh sách sản phẩm giỏ hàng
@require_http_methods(["GET", "POST"])
def cartList(request):
    try:
        # del request.session['cart']
        cart = request.session.get('cart', [])
        print(cart)

        # Tạo mảng products rỗng
        products = []
        totalAmount = 0
        # Lặp qua mỗi item trong cart
        for item in cart:
            # Lấy id và quantity từ item
            product_id = item['id']
            quantity = item['quantity']

            # Lấy sản phẩm từ cơ sở dữ liệu
            product = Product.objects.get(pk=product_id)
            amount = product.price * quantity * (1 - product.discount)
            totalAmount += amount
            # Thêm sản phẩm và quantity vào mảng products
            products.append({
                'id': product.id,
                'name': product.product_name,
                'price': product.price,
                'discount': product.discount,
                'thumbnail': product.thumbnail,
                'quantity': quantity,
                'amount': amount
            })
            #Thêm price, discount, amount vào cho cart
            item['name'] = product.product_name
            item['price'] = float(product.price)
            item['discount'] = float(product.discount)
            item['amount'] = float(amount)

        print(products)
        #Cap nhat lai cart
        request.session['cart'] = cart

        # Create a response
        response = TemplateResponse(request, "cart_list.html", {
            'products': products,
            'total': totalAmount
        }
                                    )
        # Return the response
        return response
    except Exception as e:  # Bắt lỗi cụ thể
        #TODO: Hiển thị lỗi Friendly ra app message
        raise Exception('Error: ' + str(e))


# Trang cảm ơn khi đặt hàng thành công
@require_http_methods(["GET"])
def cartThanks(request):
    # Create a response
    order_id = request.session.get('order_id', None)
    
    #Nếu giỏ hàng trống thì render trang báo giỏ hàng trống
    if not order_id:
        # Return the response
        return TemplateResponse(request, "cart_empty.html")
    
    order = Order.objects.get(id=order_id) if order_id else None

    response = TemplateResponse(request, "cart_thanks.html", {
        'order': order
    })
   

    response = TemplateResponse(request, "cart_thanks.html", {
        'order': order
    })
    # xóa đi
    if 'order_id' in request.session:
        del request.session['order_id']
    # Return the response
    return response


#Hiển thị màn hình Checkout
@require_http_methods(["GET", "POST"])
def cartCheckout(request):
    products = []
    totalAmount = 0
    cart = request.session.get('cart', [])

    if not cart:
        return TemplateResponse(request, "cart_empty.html")

    customer = request.customer

    if request.method == "POST":
        form = CheckoutForm(request.POST)

        if form.is_valid():
            customer_email = form.cleaned_data['email']
            customer_phone = form.cleaned_data['phone']

            if not customer:
                try:
                    customer = Customer.objects.get(Q(email=customer_email) | Q(phone=customer_phone))
                except Customer.DoesNotExist:
                    customer = Customer(
                        email=customer_email,
                        phone=customer_phone,
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                        street=form.cleaned_data['street'],
                        city=form.cleaned_data['city'],
                        state=form.cleaned_data['state'],
                        zip_code=form.cleaned_data['zip_code']
                    )
                    customer.save()

            order = Order(
                customer=customer,
                order_note=form.cleaned_data['order_note'],
                shipping_street=customer.street,
                shipping_city=customer.city,
                shipping_state=customer.state,
                payment_type=form.cleaned_data['payment_type'],
            )
            order.save()

            for item in cart:
                product_id = item['id']
                product = Product.objects.get(id=product_id)
                order_item = OrderItem(
                    order=order,
                    product=product,
                    price=item['price'],
                    quantity=item['quantity'],
                    discount=item.get('discount', 0),
                )
                order_item.save()

            del request.session['cart']
            request.session['order_id'] = order.id

            return HttpResponseRedirect("/cart/thanks/")

    else:
        if customer:
            initial_data = {
                'id': customer.id,  # Thêm ID khách hàng vào dữ liệu khởi tạo
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'email': customer.email,
                'phone': customer.phone,
                'street': customer.street,
                'city': customer.city,
                'state': customer.state,
                'zip_code': customer.zip_code if customer.zip_code else '',
            }
            form = CheckoutForm(initial=initial_data)
        else:
            form = CheckoutForm()

        for item in cart:
            product_id = item['id']
            product = Product.objects.get(pk=product_id)
            totalAmount += item['amount']
            products.append({
                'id': product.id,
                'name': product.product_name,
                'price': item['price'],
                'discount': item['discount'],
                'thumbnail': product.thumbnail,
                'quantity': item['quantity'],
                'amount': item['amount']
            })

    response = TemplateResponse(request, "cart_checkout.html", {
        "form": form,
        "products": products,
        "total": totalAmount,
        "customer": customer
    })
    return response