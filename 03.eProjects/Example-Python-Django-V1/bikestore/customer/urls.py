from django.urls import path
from . import views

# Khai báo url cho view ở bên file view
# Tham số đầu tiên trong hàm path
# chính là URL tính tại vị trí của app product
# Tương đương với http://127.0.0.1:8000/customers/
urlpatterns = [
    path("", views.customers_dashboard, name="customer_dashboard"),
    path("profile/", views.customers_profile, name="customer_profile"),
    path("orders/", views.customers_orders, name="customer_orders"),
    path('login/', views.login_view, name='customer_login'),
    path('logout/', views.logout_view, name='customer_logout'),
    path('register/', views.register_view, name='customer_register'),
    path('forgot-password/', views.forgot_password_view, name='customer_forgot_password'),
    path('reset-password/', views.reset_password_view, name='customer_reset_password'),
]
