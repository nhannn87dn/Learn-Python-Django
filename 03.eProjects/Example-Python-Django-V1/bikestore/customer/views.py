from django.template.response import TemplateResponse
from django.shortcuts import redirect
from .forms import LoginForm, RegisterForm, ForgotPasswordForm
from django.contrib import messages
from .models import Customer
from .auth_backends import CustomerAuthBackend
from django.core.mail import EmailMessage
import random
from .decorators import customer_login_required
import logging

logger = logging.getLogger('customer.views') # Đảm bảo tên này khớp với cấu hình trong settings.py

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            auth_backend = CustomerAuthBackend()
            customer = auth_backend.authenticate(request, email=email, password=password)
            if customer is not None:
                request.session['customer_id'] = customer.id
                
                logger.info("customer.id: " + str(customer.id))
                
                return redirect('customer_dashboard')
            else:
                messages.error(request, 'Invalid email or password')
    else:
        form = LoginForm()
    
    return TemplateResponse(request, 'customers_login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            customer = form.save()
            request.session['customer_id'] = customer.id
            return redirect('customer_dashboard')
    else:
        form = RegisterForm()
    return TemplateResponse(request, 'customers_register.html', {'form': form})

def forgot_password_view(request):
    logger.info("forgot_password_view")
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                customer = Customer.objects.get(email=email)
                otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
                customer.otp = otp
                customer.save()
                
                # Send OTP via email
                email_message = EmailMessage(
                    subject='Password Reset OTP',
                    body=f'<h2>Your OTP for password reset is: <strong>{otp}</strong></h2>',
                    from_email='ecshopvietnamese@gmail.com',
                    to=[email],
                    reply_to=['ecshopvietnamese@gmail.com'],
                )
                email_message.content_subtype = "html"  # Main content is now text/html
                result = email_message.send()
                
                if result == 1:
                    request.session['reset_email'] = email
                    messages.success(request, 'OTP has been sent to your email.')
                    return redirect('customer_reset_password')
                else:
                    messages.error(request, 'Failed to send OTP. Please try again.')
            except Customer.DoesNotExist:
                messages.error(request, 'No account found with this email.')
    else:
        form = ForgotPasswordForm()
    return TemplateResponse(request, 'customers_forgot_password.html', {'form': form})



def reset_password_view(request):
    logger.info("Entering reset_password_view")
    logger.info(f"Session contents: {request.session.items()}")
    
    if 'reset_email' not in request.session:
        logger.warning("reset_email not in session. Redirecting to login.")
        return redirect('customer_login')
    
    logger.info(f"reset_email found in session: {request.session['reset_email']}")
    
    if request.method == 'POST':
        otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        email = request.session['reset_email']
        
        try:
            customer = Customer.objects.get(email=email)
            if customer.otp == otp:
                customer.set_password(new_password)
                customer.otp = None
                customer.is_verify = True # xác thực Email
                customer.save()
                del request.session['reset_email']
                messages.success(request, 'Password has been reset successfully.')
                return redirect('customer_login')
            else:
                messages.error(request, 'Invalid OTP.')
        except Customer.DoesNotExist:
            messages.error(request, 'No account found with this email.')
    
    return TemplateResponse(request, 'customers_reset_password.html')

def logout_view(request):
    if 'customer_id' in request.session:
        del request.session['customer_id']
    return redirect('customer_login')

@customer_login_required
def customers_dashboard(request):
    context = {
        'customer': request.customer
    }
    return TemplateResponse(request, "customers_dashboard.html", context)
@customer_login_required
def customers_profile(request):
    # request.customer có được từ middleware
    customer = request.customer
    context = {
        'customer': customer,
        'profile_info': {
            'Full Name': f"{customer.first_name} {customer.last_name}",
            'Email': customer.email,
            'Phone': customer.phone,
            'Birthday': customer.birthday,
            'Address': f"{customer.street}, {customer.city}, {customer.state}",
            'Zip Code': customer.zip_code,
            'Member Since': customer.created_at.strftime('%B %d, %Y'),
        }
    }
    return TemplateResponse(request, "customers_profile.html", context)

@customer_login_required
def customers_orders(request):
    # Implement order retrieval logic here
    context = {
        'customer': request.customer,
        'orders': []  # Replace with actual orders
    }
    return TemplateResponse(request, "customers_orders.html", context)