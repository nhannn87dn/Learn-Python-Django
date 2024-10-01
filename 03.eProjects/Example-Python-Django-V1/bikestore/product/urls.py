from django.urls import path
from . import views

# Khai báo url cho view ở bên file view
# Tham số đầu tiên trong hàm path
# chính là URL tính tại vị trí của app product
# Tương đương với http://127.0.0.1:8000/products/
urlpatterns = [
    path("", views.productList, name="product-list"),
    path("<int:id>", views.productDetail, name="product-detail"),
]
# product-list là tên bạn đặt cho view, không được trùng nhau trong cả project