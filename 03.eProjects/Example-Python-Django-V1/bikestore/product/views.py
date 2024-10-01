from django.template.response import TemplateResponse
from .models import Product
from category.models import Category
from brand.models import Brand
from django.core.paginator import Paginator


#Hiển thị danh sách sản phẩm
def productList(request):
    #Lấy danh sách categories
    categories = Category.objects.all()

    #Lấy danh sách brand
    brands = Brand.objects.all()

    # Bắt đầu với truy vấn cơ bản
    products_list = Product.objects.filter(is_delete=0, is_active=1)

    # Lấy các tham số truy vấn tùy chọn
    category = int(request.GET.get('category', 0))
    brand = int(request.GET.get('brand', 0))
    sort_by = request.GET.get('sort_by', 'updated_at')
    sort_type = request.GET.get('sort_type', 'DESC')

    # Lọc theo category nếu có
    if category > 0:
        products_list = products_list.filter(category=category)

    # Lọc theo brand nếu có
    if brand > 0:
        products_list = products_list.filter(brand=brand)

    # Sắp xếp nếu có
    if sort_by and sort_type:
        sort_order = f"{'-' if sort_type.lower() == 'desc' else ''}{sort_by}"
        products_list = products_list.order_by(sort_order)

    # Số lượng sản phẩm trên mỗi trang, tại dòng này vẫn chưa truy vấn
    paginator = Paginator(products_list, 12)  # Hiển thị 12 sản phẩm trên mỗi trang

    # Lấy số trang hiện tại từ request
    page_number = request.GET.get('page', 1)

    try:
        page_number = int(page_number)
    except ValueError:
        page_number = 1

    # Tính toán chỉ số bắt đầu và kết thúc cho slicing
    start_index = (page_number - 1) * paginator.per_page
    end_index = start_index + paginator.per_page

    # Slicing QuerySet để chỉ lấy các bản ghi cần thiết
    page_obj = products_list[start_index:end_index]

    # Tạo đối tượng Page cho template, bắt đầu truy vấn
    page = paginator.page(page_number)
    page.object_list = page_obj

    #Truyền các biến xuống template
    context = {
        #"products": products_list, #không có phân trang
        "products_page": page,  # Đã phân trang
        "categories": categories,
        "brands": brands
    }
    # Create a response
    response = TemplateResponse(request, "product_list.html", context)

    # Return the response
    return response


#Hiển thị chi tiết sản phẩm
def productDetail(request, id):
    #Lấy thông tin sản phẩm có id
    product = Product.objects.get(pk=id)
    #Truyền các biến xuống template
    context = {
        "product": product,
    }
    # Create a response
    response = TemplateResponse(request, "product_detail.html", context)

    # Return the response
    return response
